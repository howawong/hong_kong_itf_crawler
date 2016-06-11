import json
OTHERS = 'Others'
UNIVERSITIES = 'Universities'
class Project:
    def __init__(self, d):
        self.category    = d.get('category', OTHERS)
        self.title       = d.get('Project Title', OTHERS)
        self.coordinator = d.get('Project Coordinator', OTHERS)
        self.period = d.get('Project Period', OTHERS)
        self.reference = d.get('Project Reference', None)
        self.team = d.get('Research Team', OTHERS)
        self.programme = d.get('Programme', 'Nil')
        self.institute = d.get('Applicant Institute', OTHERS)
        self.organization = d.get('Applicant Organization', OTHERS)
        self.deputy = d.get('Deputy Project Coordinator', OTHERS)
        self.recipient = d.get('Recipient Organization', OTHERS)
        self.sponsor = d.get('Sponsor(s)/Supporting Party(ies)', OTHERS)
        self.lead = d.get('Lead Applicant', OTHERS)
        self.co_applicant = d.get('Co-Applicant', OTHERS)
        self.fund = int(d.get('Funds Approved (HK$\'000)', "0").replace(",", "")) / 1000.0
    
    def is_others(self):
        return self.recipient not in ['The Hong Kong Applied Science and Technology Research Institute Company Limited', 'The Chinese University of Hong Kong', 'The Hong Kong Polytechnic University', 'Nano and Advanced Materials Institute Limited', 'The University of Hong Kong', 'The Hong Kong University of Science and Technology', 'City University of Hong Kong', 'The Hong Kong Research Institute of Textiles and Apparel Limited', 'Hong Kong Productivity Council', 'Hong Kong R&D Centre for Logistics and Supply Chain Management Enabling Technologies Limited', 'The Hong Kong Research Institute of Textiles and Apparel Limited', 'City University of Hong Kong', 'Automotive Parts and Accessory Systems R&D Centre', 'Hong Kong Science and Technology Parks Corporation', 'Hong Kong Institute of Biotechnology Limited', 'Hong Kong Cyberport Management Company Limited', 'Hong Kong Baptist University', 'Innovation and Technology Commission', 'The Hong Kong University of Science and Technology (Consortium)', 'GS1 Hong Kong Limited', 'Hong Kong Metal Finishing Society Limited', 'Hong Kong Wireless Technology Industry Association Limited', 'Hong Kong Jewelry Manufacturers\' Association', 'Hong Kong Plastic Machinery Association Limited', 'Hong Kong Watch Manufacturers Association Limited', 'Hong Kong Plastics Technology Centre Limited']

    def is_uni(self):
        return self.recipient in ['The Chinese University of Hong Kong', 'The Hong Kong University of Science and Technology', 'The Hong Kong Polytechnic University', 'The University of Hong Kong', 'City University of Hong Kong', 'Hong Kong Baptist University', 'The Hong Kong University of Science and Technology (Consortium)']

    def get_months(self):
        d = self.period.split(" ")
        d_from = d[0]
        d_to = d[2]
        day_from, month_from, year_from = [int(x) for x in d_from.split("/")]
        day_to,  month_to, year_to = [int(x) for x in d_to.split("/")]
        a = month_from
        b = year_from
        dates = ["%d-%.2d" % (b, a)]
        while a != month_to or b != year_to:
            a = a + 1
            if a == 13:
                b = b + 1
                a = 1
            dates.append("%d-%.2d" % (b, a))
        return dates


def load_projects(file_name="projects.json"):
    items = json.loads(open(file_name, 'rb').read())
    return [Project(d) for d in items["All"]]
