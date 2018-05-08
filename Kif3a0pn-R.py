# -*- coding: utf-8 -*-
"""
本程序用来模拟kinesin在MT上的运动
"""

#0pN-Hsk

#导入需要的包

import numpy as np

#设置随机数种子myseed

myseed = 5    
        
#kinesin的状态用K表示
#K = 0 #T--T（T->ATP,D->ADP,O->空,DP->ADP.Pi）
#K = 1 #DP--T
#K = 2 #T--DP
K = 0

#设置化学反应速率DmkWT0pN

kH = 350 #T->DP
kc = 150 #DP->D
rho = 17 #前后头扔Pi速率比（后头快）
kD = 90 # D->O
phi = 1 #前后头扔ADP速率比（前头快）
kNL_T = 1.0 #ATP dock速率
kNL_DP = 1200.0 #ADP.Pi dock速率
kb = 2.0 #ATP结合速率
ATPc = 2000.0 #ATP浓度
kcm = 10.22 #中间态扔Pi速率
kout = 1.43 #中间态ADP头脱离的速率
d = 8.2 #步长

#设置机械步概率和时间

#DP--T->D--T
P13 = 0.073
t13 = 0.0

#DP--T->T*D
P14 = 0.85
t14 = 0.0

#DP--T->T--D
P15 = 0.077
t15 = 0.0

#T--DP->D--T
P23 = 0.0
t23 = 0.0

#T--DP->T--D
P25 = 1
t25 = 0.0

#T*D->D--T
P43 = 0.0
t43 = 0.0

#T*D->T--D
P45 = 1
t45 = 0.0

#DP--DP->D--DP
P67 = P13
t67 = 0.0

#DP--DP->DP*D
P69 = P14
t69 = 0.0

#DP--DP->DP--D
P610 = P15
t610 = 0.0

#DP--DP->D--DP
P67f = P23
t67f = 0.0


#DP--DP->DP--D
P610f = P25
t610f = 0.0

#D--DP->D--D
P713 = 0.06
t713 = 0.0

#D--DP->D*D
P714 = 0.757
t714 = 0.0


#D--DP->D--D
P713f = 0.183
t713f = 0.0

#DP*D->D--DP
P97 = P43
t97 = 0.0


#DP*D->DP--D
P910 = P45
t910 = 0.0

#DP--D->D--D
P1013 = P13
t1013 = 0.0

#DP--D->D*D
P1014 = P14
t1014 = 0.0


#DP--D->D--D
P1013f = P15
t1013f = 0.0

#O--DP->D--O
P1216 = P713
t1216 = 0.0

#O--DP->O*D
P1217 = P714
t1217 = 0.0


#O--DP->O--D
P1218 = P713f
t1218 = 0.0

#DP--O->D--O
P1516 = P13
t1516 = 0.0

#DP--O->O*D
P1517 = P14
t1517 = 0.0


#DP--O->O--D
P1518 = P15
t1518 = 0.0

#kinesin运动的时间由T表示

T = 0.0

#kinesin的位置（后头位置）由X表示

X = 0.0

#模拟次数N

N = 200

#记录每次模拟的runlength--R

R = []

#记录每次模拟的速度V

V = []

#模拟开始

np.random.seed(myseed)

for index in range(N):
    K = 0 #初始状态：T--T
    T = 0.0
    X = 0.0
    while 1:
        K_now = K #记录当前状态
        
        if K_now == 0: #T--T
            kT = kH + kH
            T = T + (np.random.exponential(1.0/kT))
            decision_ch = np.random.random() #化学步选择
            if decision_ch <= kH / kT: #后头水解
                K = 1 #DP--T
            else: #前头水解
                K = 2 #T--DP
            
        if K_now == 1: #DP--T
            kT = kc + kH
            T = T + (np.random.exponential(1.0/kT))
            decision_ch = np.random.random() #化学步选择
            if decision_ch <= kc / kT: #后头扔Pi
                decision_mh = np.random.random() #机械步选择
                if decision_mh <= P13:#DP--T->D--T，用时t13
                    K = 3 #D--T
                    #T = T + (np.random.exponential(t13))
                elif decision_mh <= (P13 + P14):#DP--T->T*D，用时t14
                    K = 4 #T*D
                    #T = T + (np.random.exponential(t14))
                    X = X + (1 * d)
                else: #DP--T->T--D，用时t15
                    K = 5 #T--D
                    #T = T + (np.random.exponential(t15))
                    X = X + (1 * d)
            else: #前头水解
                K = 6 #DP--DP
                
        if K_now == 2: #T--DP
            kT = kc / rho + kH
            T = T + (np.random.exponential(1.0/kT))
            decision_ch = np.random.random() #化学步选择
            if decision_ch <= kc / rho / kT: #前头扔Pi
                decision_mh = np.random.random() #机械步选择
                if decision_mh <= P23:#T--DP->D--T，用时t23
                    K = 3 #D--T
                    #T = T + (np.random.exponential(t23))
                    X = X + (-1 * d)
                else: #T--DP->T--D，用时t25
                    K = 5 #T--D
                    #T = T + (np.random.exponential(t25))
            else: #后头水解
                K = 6 #DP--DP            

        if K_now == 3: #D--T
            kT = kD / phi + kH
            T = T + (np.random.exponential(1.0/kT))
            decision_ch = np.random.random() #化学步选择
            if decision_ch <= kH / kT: #前头水解
                K = 7 #D--DP
            else: #后头扔ADP
                K = 8 #O--T
                
        if K_now == 4: #T*D
            kT = kH + kNL_T
            T = T + (np.random.exponential(1.0/kT))
            decision_ch = np.random.random() #化学步选择
            if decision_ch <= kH / kT: #结合头水解
                K = 9 #DP*D
            else: #结合头dock
                decision_mh = np.random.random() #机械步选择
                if decision_mh <= P43:#T*D->D--T，用时t43
                    K = 3 #D--T
                    #T = T + (np.random.exponential(t43))
                    X = X + (-1 * d)
                else: #T*D->T--D，用时t45
                    K = 5 #T--D
                    #T = T + (np.random.exponential(t45))
        
        if K_now == 5: #T--D
            kT = kD + kH
            T = T + (np.random.exponential(1.0/kT))
            decision_ch = np.random.random() #化学步选择
            if decision_ch <= kH / kT: #后头水解
                K = 10 #DP--D
            else: #前头扔ADP
                K = 11 #T--O
                
        if K_now == 6: #DP--DP
            kT = kc + kc / rho
            T = T + (np.random.exponential(1.0/kT))
            decision_ch = np.random.random() #化学步选择
            if decision_ch <= kc / kT: #后头扔Pi
                decision_mh = np.random.random() #机械步选择
                if decision_mh <= P67:#DP--DP->D--DP，用时t67
                    K = 7 #D--DP
                    #T = T + (np.random.exponential(t67))
                elif decision_mh <= (P67 + P69):#DP--DP->DP*D，用时t69
                    K = 9 #DP*D
                    #T = T + (np.random.exponential(t69))
                    X = X + (1 * d)
                else: #DP--DP->DP--D，用时t610
                    K = 10 #DP--D
                    #T = T + (np.random.exponential(t610))
                    X = X + (1 * d)
            else: #前头扔Pi
                decision_mh = np.random.random() #机械步选择
                if decision_mh <= P67f:#DP--DP->D--DP，用时t67f
                    K = 7 #D--DP
                    #T = T + (np.random.exponential(t67f))
                    X = X + (-1 * d)
                else: #DP--DP->DP--D，用时t610f
                    K = 10 #DP--D
                    #T = T + (np.random.exponential(t610f))

        if K_now == 7: #D--DP
            kT = kD / phi + kc / rho
            T = T + (np.random.exponential(1.0/kT))
            decision_ch = np.random.random() #化学步选择
            if decision_ch <= kD / phi / kT: #后头扔ADP
                K = 12 #O--DP
            else: #前头扔Pi
                decision_mh = np.random.random() #机械步选择
                if decision_mh <= P713:#D--DP->D--D，用时t713
                    K = 13 #D--D
                    #T = T + (np.random.exponential(t713))
                    X = X + (-1 * d)
                elif decision_mh <= P713 + P714: #D--DP->D*D，用时t714
                    K = 14 #D*D
                    #T = T + (np.random.exponential(t714))
                else: #D--DP->D--D，用时t713f
                    K = 13 #D--D
                    #T = T + (np.random.exponential(t713f))
                    
        if K_now == 8: #O--T
            kT = kb * ATPc + kH
            T = T + (np.random.exponential(1.0/kT))
            decision_ch = np.random.random() #化学步选择
            if decision_ch <= kH / kT: #前头水解
                K = 12 #O--DP
            else: #后头结合ATP
                K = 0 #T--T
                
        if K_now == 9: #DP*D
            kT = kcm + kNL_DP
            T = T + (np.random.exponential(1.0/kT))
            decision_ch = np.random.random() #化学步选择
            if decision_ch <= kNL_DP / kT: #结合头dock
                decision_mh = np.random.random() #机械步选择
                if decision_mh <= P97:#DP*D->D--DP，用时t97
                    K = 7 #D--DP
                    #T = T + (np.random.exponential(t97))
                    X = X + (-1 * d)
                else: #DP*D->DP--D，用时t910
                    K = 10 #DP--D
                    #T = T + (np.random.exponential(t910))
            else: #结合头扔Pi，掉了
                break
                
        if K_now == 10: #DP--D
            kT = kc + kD
            T = T + (np.random.exponential(1.0/kT))
            decision_ch = np.random.random() #化学步选择
            if decision_ch <= kc / kT: #后头扔Pi
                decision_mh = np.random.random() #机械步选择
                if decision_mh <= P1013:#DP--D->D--D，用时t1013
                    K = 13 #D--D
                    #T = T + (np.random.exponential(t1013))
                elif decision_mh <= (P1013 + P1014):#DP--D->D*D，用时t1014
                    K = 14 #D*D
                    #T = T + (np.random.exponential(t1014))
                    X = X + (1 * d)
                else: #DP--D->D--D，用时t1013f
                    K = 13 #D--D
                    #T = T + (np.random.exponential(t1013f))
                    X = X + (1 * d)
            else: #前头扔ADP
                K = 15 #DP--O
                
        if K_now == 11: #T--O
            kT = kb * ATPc + kH
            T = T + (np.random.exponential(1.0/kT))
            decision_ch = np.random.random() #化学步选择
            if decision_ch <= kH / kT: #后头水解
                K = 15 #DP--O
            else: #前头结合ATP
                K = 0 #T--T
                
        if K_now == 12: #O--DP
            kT = kb * ATPc + kc / rho
            T = T + (np.random.exponential(1.0/kT))
            decision_ch = np.random.random() #化学步选择
            if decision_ch <= kb * ATPc / kT: #后头结合ATP
                K = 2 #T--DP
            else: #前头扔Pi
                decision_mh = np.random.random() #机械步选择
                if decision_mh <= P1216:#O--DP->D--O，用时t1216
                    K = 16 #D--O
                    #T = T + (np.random.exponential(t1216))
                    X = X + (-1 * d)
                elif decision_mh <= P1216 + P1217:#O--DP->O*D，用时t1217
                    K = 17 #O*D
                    #T = T + (np.random.exponential(t1217))
                else: #O--DP->O--D，用时t1218
                    K = 18 #O--D
                    #T = T + (np.random.exponential(t1218))
                    
        if K_now == 13: #D--D
            kT = kD / phi + kD
            T = T + (np.random.exponential(1.0/kT))
            decision_ch = np.random.random() #化学步选择
            if decision_ch <= kD / phi / kT: #后头扔ADP
                K = 18 #O--D
            else: #前头扔ADP
                K = 16 #D--O
                
        if K_now == 14: #D*D
            kT = kD + kout
            T = T + (np.random.exponential(1.0/kT))
            decision_ch = np.random.random() #化学步选择
            if decision_ch <= kD / kT: #结合头扔ADP
                K = 17 #O*D
            else: #脱离
                break
                
        if K_now == 15: #DP--O
            kT = kc + kb * ATPc
            T = T + (np.random.exponential(1.0/kT))
            decision_ch = np.random.random() #化学步选择
            if decision_ch <= kc / kT: #后头扔Pi
                decision_mh = np.random.random() #机械步选择
                if decision_mh <= P1516:#DP--O->D--O，用时t1516
                    K = 16 #D--O
                    #T = T + (np.random.exponential(t1516))
                elif decision_mh <= (P1516 + P1517):#DP--O->O*D，用时t1517
                    K = 17 #O*D
                    #T = T + (np.random.exponential(t1517))
                    X = X + (1 * d)
                else: #DP--O->O--D，用时t1518
                    K = 18 #O--D
                    #T = T + (np.random.exponential(t1518))
                    X = X + (1 * d)
            else: #前头结合ATP
                K = 1 #DP--T
                
        if K_now == 16: #D--O
            kT = kD / phi + kb * ATPc
            T = T + (np.random.exponential(1.0/kT))
            decision_ch = np.random.random() #化学步选择
            if decision_ch <= kD / phi / kT: #后头扔ADP
                K = 19 #O--O
            else: #前头结合ATP
                K = 3 #D--T
                
        if K_now == 17: #O*D
            kT = kb * ATPc
            T = T + (np.random.exponential(1.0/kT))
            decision_ch = np.random.random() #化学步选择
            if decision_ch <= kb * ATPc / kT: #结合头结合ATP
                K = 4 #T*D

        if K_now == 18: #O--D
            kT = kD + kb * ATPc
            T = T + (np.random.exponential(1.0/kT))
            decision_ch = np.random.random() #化学步选择
            if decision_ch <= kD / kT: #前头扔ADP
                K = 19 #O--O
            else: #后头结合ATP
                K = 5 #T--D
                
        if K_now == 19: #D--O
            kT = kb * ATPc + kb * ATPc
            T = T + (np.random.exponential(1.0/kT))
            decision_ch = np.random.random() #化学步选择
            if decision_ch <= kb * ATPc / kT: #后头结合ATP
                K = 11 #T--O
            else: #前头结合ATP
                K = 8 #O--T
                
#        if T > 20: #每条轨迹20s
#            break
            
    V.append(np.sum(X)/np.sum(T))
    R.append(np.sum(X))
    
print(np.mean(R))
print(np.mean(V))
