from django.shortcuts import render
from .models import *
from .forms import JobFilterForm
from django.db.models import Count, Q
import json
from datetime import datetime


def dashboard(request):

    date_range = request.GET.get('date_range')
    company_name = request.GET.get('company')
    job_type_name = request.GET.get('job_type')
    location_name = request.GET.get('location')

    start_date = end_date = None
    joblisiting_filter = Q()
    second_joblisiting_filter = Q()
    
    if date_range  :
        start_date, end_date = date_range.split(' - ')
        start_date = datetime.strptime(start_date, '%m/%d/%Y')
        end_date = datetime.strptime(end_date, '%m/%d/%Y')
        joblisiting_filter &= Q(joblistings__conditionid__scrapping_date__range=[start_date, end_date])
        second_joblisiting_filter &= Q(conditionid__scrapping_date__range=[start_date, end_date])

    if company_name:
        joblisiting_filter &= Q(joblistings__companyid__company_name=company_name)
        second_joblisiting_filter &= Q(companyid__company_name=company_name)
        
    if location_name :
        joblisiting_filter &= Q(joblistings__locationid__city=str(location_name))
        second_joblisiting_filter &= Q(locationid__city=str(location_name))


    if job_type_name :
        joblisiting_filter &= Q(joblistings__jobtypeid__job_type=job_type_name)
        second_joblisiting_filter &= Q(locationid__city=str(location_name))

    
    # Job Listings by Company
    job_count_by_company = Companies.objects.annotate(
        job_count=Count('joblistings', filter=joblisiting_filter)
    ).order_by('-job_count')
    
    job_count_by_company_data = [
        {'company_name': company.company_name, 'job_count': company.job_count}
        for company in job_count_by_company
    ]
    

    # Job Listings by Location
    job_count_by_location = Locations.objects.annotate(job_count=Count('joblistings', filter=joblisiting_filter)).order_by('-job_count')
    job_count_by_location_data = [
        {'city': location.city, 'job_count': location.job_count}
        for location in job_count_by_location
    ]
    

    # Job Listings by Sector
    job_count_by_sector = Sectors.objects.annotate(job_count=Count('joblistings', filter=joblisiting_filter)).order_by('-job_count')
    job_count_by_sector_data = [
        {'sector': sector.sector, 'job_count': sector.job_count}
        for sector in job_count_by_sector
    ]
    

    # Job Listings by Job Type
    job_count_by_job_type = JobTypes.objects.annotate(job_count=Count('joblistings', filter=joblisiting_filter)).order_by('-job_count')
    job_count_by_job_type_data = [
        {'job_type': job_type.job_type, 'job_count': job_type.job_count}
        for job_type in job_count_by_job_type
    ]


    # Remote vs On-site Job Listings
    remote_vs_onsite = Locations.objects.values('remote_status').annotate(job_count=Count('joblistings', filter=joblisiting_filter)).order_by('-job_count')
    remote_vs_onsite_data = list(remote_vs_onsite)



    # Job Listings Over Time
    job_listings_over_time = JobConditions.objects.values('scrapping_date').annotate(job_count=Count('joblistings',filter=joblisiting_filter)).order_by('scrapping_date')

    job_listings_over_time_data = [
    {'scrapping_date': entry['scrapping_date'].strftime('%Y-%m-%d'), 'job_count': entry['job_count']}
    for entry in job_listings_over_time
]
    

    # Job Listings by Promotion Status
    promotion_effectiveness = JobConditions.objects.values('promoted_status').annotate(
            job_count=Count('joblistings', filter=joblisiting_filter)
        ).order_by('-job_count')

    promotion_effectiveness_data = list(promotion_effectiveness)

    # Applicants per Job Listing
    job_listings_with_applicants = JobListings.objects.filter(
        second_joblisiting_filter
    ).values('jobid', 'jobidlinkedin', 'applicants').order_by('-applicants')

    job_listings_with_applicants_data = list(job_listings_with_applicants)




    # Serialize data to JSON
    context = {
        'job_count_by_company_data': json.dumps(job_count_by_company_data),
        'job_count_by_location_data': json.dumps(job_count_by_location_data),
        'job_count_by_sector_data': json.dumps(job_count_by_sector_data),
        'job_count_by_job_type_data': json.dumps(job_count_by_job_type_data),
        'job_listings_with_applicants_data': json.dumps(job_listings_with_applicants_data),
        'promotion_effectiveness_data': json.dumps(promotion_effectiveness_data),
        'remote_vs_onsite_data': json.dumps(remote_vs_onsite_data),
        'job_listings_over_time_data': json.dumps(job_listings_over_time_data),
        'locations' : Locations.objects.all(),
        'companies' : Companies.objects.all(),
        'locations' : Locations.objects.all(),
        'job_types' : JobTypes.objects.all()
    }
    
    return render(request, 'filtersAnalytics/dashboard.html', context)

def home(request):
    return render(request, 'base.html')