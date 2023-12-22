import random
import os
def get_faults(module):
    
    flist_path = f'./{module}_stuck_full.fault'
    fold_path = f'./faults_dt_{module}'
    file_names = os.listdir(fold_path)
    file = open(flist_path, 'r')
    faults = file.read().split('\n')
    file.close()
    return faults
def get_p2f_and_f2p(fold_Path,rm_hard=False):
    f2p = {}
    f2p_num = {}
    p2f = {}
    p2f_num = {}
    file_names = os.listdir(fold_Path)
    for file_name in file_names:
        idx = int(file_name[9:])
        path = f'{fold_Path}/{file_name}'
        file = open(path, 'r')
        lines = file.read().split('\n')
        for line in lines:
            if f2p.get(line)==None:
                f2p[line] = []
            f2p[line].append(idx)
            if idx not in p2f:
                p2f[idx] = []
            p2f[idx].append(line)
            p2f_num[idx] = len(p2f[idx])
        file.close()
    for f, p in f2p.items():
        f2p_num[f] = len(p)
    return p2f,f2p,p2f_num, f2p_num

def random_sel(faults, module, target_rate):
    p2f, f2p, p2f_num, f2p_num = get_p2f_and_f2p(f'./faults_dt_{module}')
    total = len(faults)
    target = total * target_rate
    fault_state = dict(zip(faults,[1 for i in range(total)]))
    p2f_num_new = p2f_num.copy()
    p2f_new = p2f.copy()
    detected_fault_num = 0
    selected = []
    while detected_fault_num < target:
        key = random.choice(list(p2f_new.keys()))
        selected.append(key)
        p2f_new.pop(key)
        fault_num = p2f_num[key]
        for f in p2f[key]:
            if fault_state[f] == 0:
                continue
            fault_state[f] = 0
            detected_fault_num += 1
            for p in f2p[f]:
                if p==key:
                    continue
                p2f_num_new[p] -= 1
    return selected
def greedy_sel_bottomup(faults, module, target_rate):
    p2f, f2p, p2f_num, f2p_num = get_p2f_and_f2p(f'./faults_dt_{module}')
    total = len(faults)
    target = total * target_rate
    fault_state = dict(zip(faults,[1 for i in range(total)]))
    p2f_num_new = p2f_num.copy()
    p2f_new = p2f.copy()
    detected_fault_num = 0
    selected = []
    detected_fault = []
    while detected_fault_num < target:
        key = max(p2f_num_new, key=p2f_num_new.get)
        selected.append(key)
        p2f_new.pop(key)
        for f in p2f[key]:
            if fault_state[f] == 0:
                continue
            fault_state[f] = 0
            detected_fault.append(f)
            detected_fault_num += 1
            for p in f2p[f]:
                if p==key:
                    continue
                p2f_num_new[p] -= 1
        p2f_num_new.pop(key)
    return selected

def greedy_sel_topdown(faults, module, target_rate):
    p2f, f2p, p2f_num, f2p_num = get_p2f_and_f2p(f'./faults_dt_{module}')
    total = len(faults)
    target = total * target_rate
    fault_state = dict(zip(faults,[1 for i in range(total)]))
    pattern_state = dict(zip([i for i in range(len(p2f.keys()))],[1 for i in range(total)]))
    p2f_num_new = p2f_num.copy()
    f2p_num_new = f2p_num.copy()
    p2f_new = p2f.copy()
    rm_fault_num = 0
    removed = []
    rm_fault = []
    while rm_fault_num < total-target:    
        key = min(p2f_num_new, key=p2f_num_new.get)
        p2f_new.pop(key)
        for f in p2f[key]:
            if fault_state[f] == 0:
                continue
            f2p_num_new[f] -= 1
            if f2p_num_new[f] == 0:
                fault_state[f] = 0
                rm_fault_num += 1
                rm_fault.append(f)
                for p in f2p[f]:
                    if p==key or pattern_state[p]==0:
                        continue
                    p2f_num_new[p] -= 1
        if rm_fault_num >= total-target:
            break
        removed.append(key)
        pattern_state[key] = 0
        p2f_num_new.pop(key)
    selected = list(set([i for i in range(len(p2f.keys()))])-set(removed))
    return selected

if __name__ == '__main__':
    module = 's400'

    faults = get_faults(module)
    selected = random_sel(faults, module, 0.9)
    print(selected,len(selected))
    
    # selected = greedy_sel_topdown(faults, module, 0.9)
    # print(len(selected))
    selected = greedy_sel_bottomup(faults, module, 0.9)
    print(selected,len(selected))
    # main()