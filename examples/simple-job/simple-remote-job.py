import dcp
dcp.init()
import pythonmonkey as pm

remote_origin = 'http://192.168.0.126:5001'

def URL(url):
    return pm.eval('(x) => new URL(x)')(url)

input_set = [3, 9, 11, 23, 45, 234, 463, 1245, 2356, 157324]

def work_function(x, a, json_str, c):
    dcp.progress()
    import json
    data = json.loads(json_str)
    b = data['Belleville-General']
    return x**2 + a * b + c

job = dcp.compute_for(input_set, work_function, [4, URL(f'{remote_origin}/data'), 5])

job.computeGroups = [{'joinKey': 'anu', 'joinSecret': 'sv92hk'}]
job.public.name = 'Simple remote job'

job.on('readystatechange', lambda s: print(f"State: {s}"))
job.on('accepted', lambda _: print(f"  Job ID: {job.id}\n  Job accepted, awaiting results..."))
job.on('result', lambda r: print(f"    ✓ result: {int(r.sliceNumber)} of {len(input_set)}, {r.result}"))
job.on('error', lambda e: print(e))

job.setResultStorage(f'{remote_origin}/results', {'elementType': 'results'})
job.exec()
job.wait()
print('Done.')