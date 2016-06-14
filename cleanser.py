import json
from project import Project
with open('projects_uncleansed.json', 'rb') as f:
    d = json.loads(f.read())
    categories_by_ref = {}
    for key in d.keys():
        if key not in ["All", "Others"]:
            project_dicts = d[key]
            for project_dict in project_dicts:
               project = Project(project_dict) 
               if project.reference not in categories_by_ref:
                   categories_by_ref[project.reference] = set()
               categories_by_ref[project.reference].add(key)
    all_project_dicts = d["All"]
    projects = []
    for project_dict in all_project_dicts:
        project = Project(project_dict)
        project.categories = list(categories_by_ref[project.reference]) if project.reference in categories_by_ref else []
        projects.append(project)
    print "Total Number of Projects: %d" % (len(projects))
    o = open("projects.json", "w")
    o.write(json.dumps([p.__dict__ for p in projects]))
    o.close()
