import dcp
dcp.init()

inputSet = [3, 9, 11, 23, 45, 234, 463, 1245, 2356, 157324]

def func(x, a, b, c):
    dcp.progress()
    return x**2 + a * b + c

job = dcp.compute_for(inputSet, func, [2, 4, 5])

job.computeGroups = [{'joinKey': 'anu', 'joinSecret': 'sv92hk'}]
job.public.name = 'Simple job'

job.on('readystatechange', lambda s: print(f"State: {s}"))
job.on('accepted', lambda _: print(f"  Job ID: {job.id}\n  Job accepted, awaiting results..."))
job.on('result', lambda r: print(f"    ✓ result: {int(r.sliceNumber)} of {len(inputSet)}, {r.result}"))
job.on('error', lambda e: print(e))

job.exec(0.007)
results = job.wait()
print('Done.')