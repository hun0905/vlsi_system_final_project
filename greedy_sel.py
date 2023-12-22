import os
import random
def remove_min_n_faults(f2p,p2f,p2f_num,n):
    f2p_num = [(len(v),k) for k,v in f2p.items()]
    min_n_faults = [f for n, f in sorted(f2p_num, key=lambda x: x[0])[:n]]
    for f in min_n_faults:
        for p in f2p[f]:
            p2f[p].remove(f)
            p2f_num[p] -=1
    return f2p,p2f,p2f_num
def get_p2f_and_f2p(fold_Path,rm_hard=False):
    f2p = {}
    p2f = {}
    p2f_num = {}
    file_names = os.listdir(fold_Path)
    for i,file_name in enumerate(file_names):
        path = f'{fold_Path}/{file_name}'
        file = open(path, 'r')
        lines = file.read().split('\n')
        for line in lines:
            if line not in f2p:
                f2p[line] = []
            f2p[line].append(i)
            if i not in p2f:
                p2f[i] = []
            p2f[i].append(line)
            p2f_num[i] = len(p2f[i])
        file.close()
    return p2f,f2p,p2f_num
def get_max(p2f, p2f_num, f2p):
    key = max(p2f_num, key=p2f_num.get)
    fault_num = p2f_num[key]
    # print(len(p2f[key]))
    for f in p2f[key]:
        f2p[f].remove(key)
        for p in f2p[f]:
            p2f[p].remove(f)
            p2f_num[p] -=1
    p2f.pop(key)
    p2f_num.pop(key)
    return fault_num,key
def get_random(p2f, p2f_num, f2p):
    key = random.choice(list(p2f.keys()))
    fault_num = p2f_num[key]
    # print(len(p2f[key]))
    for f in p2f[key]:
        f2p[f].remove(key)
        for p in f2p[f]:
            p2f[p].remove(f)
            p2f_num[p] -=1
    p2f.pop(key)
    p2f_num.pop(key)
    return fault_num,key

def get_pattern_idx_greedy(flist_path,target_value=0.7, rm_hard=False, rm_percent=0, module= 's400'):
    total = 0
    file = open(flist_path, 'r')
    total = len(file.readlines())
    target = total * target_value
    detected_now = 0
    selected = []
    p2f, f2p, p2f_num = get_p2f_and_f2p(f'./faults_dt_{module}')
    if rm_hard:
        f2p, p2f, p2f_num =remove_min_n_faults(f2p,p2f,p2f_num,int(total*(1-target_value)*rm_percent))
    while detected_now < target:
        detected, key = get_max(p2f, p2f_num, f2p)
        detected_now += detected
        selected.append(str(key))
    print('Greedy selection done(from 0 to target).')
    print(f'Final selected pattern ({len(selected)}): ',', '.join(selected))
    print('Total detected %: ',round(detected_now/total*100,2))
    print('\n')
    return selected
def get_pattern_idx_random(flist_path,target_value=0.7, rm_hard=False, rm_percent=0, module= 's400'):
    total = 0
    file = open(flist_path, 'r')
    total = len(file.readlines())
    target = total * target_value
    detected_now = 0
    selected = []
    p2f, f2p, p2f_num = get_p2f_and_f2p(f'./faults_dt_{module}')
    if rm_hard:
        f2p, p2f, p2f_num =remove_min_n_faults(f2p,p2f,p2f_num,int(total*(1-target_value)*rm_percent))
    while detected_now < target:
        detected, key = get_random(p2f, p2f_num, f2p)
        detected_now += detected
        selected.append(str(key))
    print('Random selection done.')
    print(f'Final selected pattern ({len(selected)}): ',', '.join(selected))
    print('Total detected %: ',round(detected_now/total*100,2))
    print('\n')
    return selected
def get_min(p2f, p2f_num, f2p):
    # print(p2f_num)
    key = min(p2f_num, key=p2f_num.get)
    detected_rm = 0
    for f in p2f[key]:
        f2p[f].remove(key)
        if len(f2p[f]) == 0:
            detected_rm +=1
            for p in f2p[f]:
                p2f[p].remove(f)
                p2f_num[p] -=1
            f2p.pop(f)
    p2f.pop(key)
    p2f_num.pop(key)
    return detected_rm,key
def get_pattern_idx_greedy2(flist_path,target_value=0.7, rm_hard=False, rm_percent=0, module= 's400'):
    total = 0
    file = open(flist_path, 'r')
    total = len(file.readlines())
    target = total * target_value
    detected_now = total
    selected = []
    p2f, f2p, p2f_num = get_p2f_and_f2p(f'./faults_dt_{module}')

    all_patterns = list(map(str, list(p2f.keys())))
    if rm_hard:
        f2p, p2f, p2f_num =remove_min_n_faults(f2p,p2f,p2f_num,int(total*(1-target_value)*rm_percent))
    while detected_now > target:
        detected_rm, key = get_min(p2f, p2f_num, f2p)
        final_detected = detected_now
        detected_now -= detected_rm
        final_select = key
        selected.append(str(key))
    selected.remove(str(final_select))
    detected_now = final_detected
    # print(all_patterns)
    # print(selected)
    selected = [p for p in all_patterns if p not in selected]
    
    print('Greedy selection done(from target to 0).')
    print(f'Final selected pattern ({len(selected)}): ',', '.join(selected))
    print('Total detected %: ',round(detected_now/total*100,2))
    print('\n')
    return selected
# def main():
if __name__ == '__main__':
    module = 's38584'
    get_pattern_idx_greedy ('./s38584_stuck_full.fault',0.9,False,0.0, module)
    get_pattern_idx_greedy ('./s38584_stuck_full.fault',0.9,True ,0.5, module)
    get_pattern_idx_greedy2('./s38584_stuck_full.fault',0.9,False,0.0, module)
    get_pattern_idx_greedy ('./s38584_stuck_full.fault',0.9,True ,0.5, module)
    get_pattern_idx_random ('./s38584_stuck_full.fault',0.9,False,0.0, module)
    get_pattern_idx_random ('./s38584_stuck_full.fault',0.9,True ,0.5, module)
    # main()