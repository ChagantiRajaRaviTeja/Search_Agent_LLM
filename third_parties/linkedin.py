import os
import requests  # to make http request to external API that gets us linkedin information
from dotenv import load_dotenv  # to load environment variables

load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = True):
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""
    # `mock` flag is used to avoid repetitively making API requests while debugging the code, thus saving costs incurred from API calls. Make one API request with `mock` set to `false`, host the response on github as a gist, and later set `mock` to `true`.
    if mock:
        # linkedin_profile_url is url of Raw gist document
        linkedin_profile_url = "https://gist.githubusercontent.com/ChagantiRajaRaviTeja/0bf271cfa33fd8601cfd1bb715197fb2/raw/02fc48658de638086881cb83fb7f5fd872fb6a59/Raviteja.json"
        response = requests.get(
            linkedin_profile_url,
            timeout=100,
        )
    else:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header_dic = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
        response = requests.get(
            api_endpoint,
            params={"url": linkedin_profile_url},
            headers=header_dic,
            timeout=10,
        )

    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }  # filtering out unwanted info
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/chaganti-ravi-teja-533276217/",
        )
    )  # got response: {'public_identifier': 'chaganti-ravi-teja-533276217', 'profile_pic_url': 'https://s3.us-west-000.backblazeb2.com/proxycurl/person/chaganti-ravi-teja-533276217/profile?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=0004d7f56a0400b0000000001%2F20240710%2Fus-west-000%2Fs3%2Faws4_request&X-Amz-Date=20240710T172744Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=aa4681c03f3c012d22572c3842e4e43f62c1943b8bcf3b37064871c2e3d67d66', 'first_name': 'Chaganti', 'last_name': 'Ravi Teja', 'full_name': 'Chaganti Ravi Teja', 'follower_count': 207, 'headline': 'MS Student at Indian Institute of Technology, Kanpur', 'country': 'IN', 'country_full_name': 'India', 'city': 'Guntur', 'state': 'Andhra Pradesh', 'education': [{'starts_at': {'day': 1, 'month': 8, 'year': 2021}, 'ends_at': {'day': 31, 'month': 12, 'year': 2023}, 'field_of_study': 'Machine learning in audio processing', 'degree_name': "Master's degree", 'school': 'Indian Institute of Technology, Kanpur', 'school_linkedin_profile_url': None, 'school_facebook_profile_url': None, 'description': None, 'logo_url': 'https://media.licdn.com/dms/image/C510BAQEhNteRFbyBdQ/company-logo_400_400/0/1630585318049/indian_institute_of_technology_kanpur_logo?e=1728518400&v=beta&t=CVeTnaKQXkR7ddn83x2rx9par8HZGgAPAK7rywZ_wJE', 'grade': None, 'activities_and_societies': None}, {'starts_at': {'day': 1, 'month': 6, 'year': 2016}, 'ends_at': {'day': 31, 'month': 7, 'year': 2020}, 'field_of_study': 'Electrical, Electronics and Communications Engineering', 'degree_name': 'Bachelor of Technology - BTech', 'school': 'National Institute of Technology Hamirpur-Alumni', 'school_linkedin_profile_url': None, 'school_facebook_profile_url': None, 'description': None, 'logo_url': 'https://media.licdn.com/dms/image/D4D0BAQHqwBjdDXnpcg/company-logo_400_400/0/1680593123302/nith_alumni_logo?e=1728518400&v=beta&t=4mpxqwg9VmTrB13FOviKxNsYS5ttDBU31G9Lgr2NQsQ', 'grade': None, 'activities_and_societies': None}], 'connections': 207}
