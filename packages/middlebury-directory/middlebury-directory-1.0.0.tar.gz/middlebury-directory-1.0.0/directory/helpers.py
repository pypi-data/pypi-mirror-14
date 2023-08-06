# -*- coding: utf-8 -*-

# Map our names for the search inputs to the endings of the
# long names given in the directory
search_field_aliases = {
    'query': 'txtSimpleSearch',
    'last_name': 'LastName',
    'first_name': 'FirstName',
    'email': 'Samaccountname',
    'phone': 'Telephonenumber',
    'address': 'Extensionattribute3',
    'location': 'Extensionattribute4',
    'job_title': 'Title',
    'person_type': 'Type',
    'department': 'Department'
}

search_button_aliases = {
    'simple': 'ctl00$ctl00$PageContent$PageContent$middDirectoryForm$btnSimpleSearch',  # NOQA
    'advanced': 'ctl00$ctl00$PageContent$PageContent$middDirectoryForm$btnSearch'  # NOQA
}


def search_field_full_name(fields, key):
    for field in fields:
        if field.endswith(search_field_aliases[key]):
            return field


allowed_person_types = [
    "",
    "Emeritus",
    "Faculty",
    "Schools Abroad",
    "Staff",
    "Student",
    "SUMMER GRAD"
]

allowed_person_type_aliases = {
    "Summer Graduate": "SUMMER GRAD"
}


def valid_person_type(person_type):
    if person_type in allowed_person_type_aliases:
        person_type = allowed_person_type_aliases[person_type]

    return person_type in allowed_person_types


allowed_departments = [
    "",
    "-",
    "Academic Affairs",
    "Academic Affairs/Biology",
    "Admissions",
    "American Studies",
    "Arabic",
    "Arabic School",
    "Arts Center",
    "Assistant Treasurer's Office",
    "Athletics",
    "Biology",
    "Biology/Neuroscience",
    "Bookstore",
    "Bread Loaf School of English",
    "Bread Loaf Writers' Conference",
    "Budget Office",
    "Business Office",
    "Center for Careers and Internships",
    "Center for Counseling/Human Relations",
    "Center for Education in Action",
    "Center for Social Entrepreneurship",
    "Center for Teaching/Learning/Research",
    "Chaplain's Office",
    "Chemistry and Biochemistry",
    "Chinese",
    "Chinese School",
    "Classics",
    "College Store",
    "Commons Office - Atwater",
    "Commons Office - Brainerd",
    "Commons Office - Cook",
    "Commons Office - Ross",
    "Commons Office - Wonnacott",
    "Communications",
    "Communications and Marketing",
    "Community Engagement",
    "Comparative Literatures",
    "Computer Science",
    "Controller's Office",
    "Creativity & Innovation",
    "Dance",
    "Davis United World College Scholars Program",
    "Dean of Faculty's Office",
    "Dean of Students",
    "Dean of the College",
    "Dean of the College/History of Art & Architecture",
    "Dining Services",
    "Economics",
    "Education Studies",
    "English & American Literatures",
    "Environmental Affairs",
    "Environmental Studies",
    "Events Management",
    "Facilities Services",
    "Facilities Services-Bread Loaf",
    "Film and Media Culture",
    "French",
    "French School",
    "Gender",
    "Sexuality & Feminist Studies",
    "Geography",
    "Geology",
    "German",
    "Golf Course",
    "Grants & Sponsored Programs",
    "Green Mt Higher Education Consortium",
    "History",
    "History of Art & Architecture",
    "Human Resources",
    "Humanities",
    "Information Technology Services",
    "Institute for the Advancement of Hebrew",
    "Interdepartmental",
    "International & Global Studies",
    "International Programs & Off-Campus Study",
    "International Student & Scholar Services",
    "International Studies",
    "Italian",
    "Italian School",
    "Japanese School",
    "Japanese Studies",
    "Jewish Studies",
    "Language Schools Administration",
    "Language Schools at Mills",
    "Library",
    "Mathematics",
    "MiddCORE",
    "Middlebury in DC",
    "Modern Hebrew",
    "Museum of Art",
    "Music",
    "Neuroscience",
    "New England Review",
    "New England Young Writers' Conference",
    "Office of Advancement",
    "Office of Chief Risk Officer",
    "Office of the Provost",
    "Office of the Provost/Psychology",
    "Parton Center for Health and Wellness",
    "Philosophy",
    "Physics",
    "Planning and Assessment",
    "Political Science",
    "Portuguese School",
    "President Emeritus",
    "President's Office",
    "Printing and Mailing Services",
    "Programs on Creativity & Entrepreneurship",
    "Psychology",
    "Psychology/Neuroscience",
    "Public Safety",
    "Registrar's Office",
    "Religion",
    "Retail Food Operations",
    "Rikert Nordic Center",
    "Rohatyn Center for Global Affairs",
    "Russian",
    "Russian School",
    "School of Hebrew",
    "School of Korean",
    "Sciences Tech Support Services",
    "Ski School",
    "Snow Bowl",
    "Sociology/Anthropology",
    "Spanish and Portuguese",
    "Spanish School",
    "Student Accessibility Services",
    "Student Activities",
    "Student Fellowships & Health Professions",
    "Student Financial Services",
    "Student Mail Center",
    "Studio Art",
    "Theatre",
    "Vice President for Finance & Treasurer's Office",
    "Vice President for HR and Chief Risk Officer",
    "Women's and Gender Studies",
    "Writing Program"
]


def valid_department(department):
    return department in allowed_departments
