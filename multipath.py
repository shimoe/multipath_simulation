import math
import numpy as np
import matplotlib.pyplot as plt

data_list = {'amp_ratio': 0.3, 'chip': 1,
             'delay': 1.5, 'phase': 1, 'multipath': 0}
conductivity = {'concrete': 2*10 ^ (-5), 'dry_ground': 1*10 ^ (-5),
                'mid_dry_ground': 4*10 ^ (-2), 'wet_ground': 2*10 ^ (-1),
                'fresh_water': 2*10 ^ (-1), 'sea_water': 4, 'asphalt': 2*10 ^ (-5),
                'glass': 1*10 ^ (-12), 'iron': 10300000}
e_r = {'concrete': 3, 'dry_ground': 4, 'mid_dry_ground': 7, 'wet_ground': 30,
       'fresh_water': 80, 'sea_water': 20, 'asphalt': 2.7,
       'glass': 10, 'iron': math.inf}

# amp_ratio = 0.5  # 直接波とマルチパスの振幅比
# chip = 0.5  # チップ幅(0 < chip < 1) 0.1, 0.05:ナローリコレータ, 1,0.5:ワイドリコレータ
T_d = data_list["chip"] / 2
# delay = 0.3  # マルチパス遅延距離
# phase = -1  # 位相差(1: 同相, -1: 逆相)
# multipath = 0

print(data_list)
plot_list = []
for i in range(int(data_list["delay"]*100)):
    sumple = i/100
    print(data_list["delay"])
    # 遅延距離計算
    if sumple < 0:
        print("delay is minus")
        exit
    elif 0 < sumple < (1 - data_list["amp_ratio"])*T_d:
        # 赤色の部分
        print("red")
        data_list["multipath"] = (sumple * data_list["amp_ratio"]
                                  )/(1 + data_list["amp_ratio"])*T_d
    elif (1 - data_list["amp_ratio"])*T_d < sumple < (1 + data_list["amp_ratio"])*T_d:
        # 紫の部分
        print("purple")
        if data_list["phase"]:  # 同相
            data_list["multipath"] = (sumple * data_list["amp_ratio"]
                                      )/(1 + data_list["amp_ratio"])*T_d
        else:  # 逆相
            data_list["multipath"] = T_d * data_list["amp_ratio"]
    elif (1 + data_list["amp_ratio"])*T_d < sumple < data_list["chip"] - (1 + data_list["amp_ratio"])*T_d:
        # 青色の部分
        print("blue")
        data_list["multipath"] = T_d * data_list["amp_ratio"]
    elif data_list["chip"] - (1 + data_list["amp_ratio"])*T_d < sumple < data_list["chip"] - (1 - data_list["amp_ratio"])*T_d:
        # 黄色の部分
        print("yellow")
        if data_list["phase"]:  # 同相
            data_list["multipath"] = T_d * data_list["amp_ratio"]
        else:  # 逆相
            data_list["multipath"] = -data_list["amp_ratio"] * (
                data_list["chip"] + T_d - sumple)/(2 + data_list["amp_ratio"])
    elif data_list["chip"] - (1 + data_list["amp_ratio"])*T_d < sumple < data_list["chip"] + T_d:
        # 緑の部分
        print("green")
        if data_list["phase"]:  # 同相
            data_list["multipath"] = data_list["amp_ratio"] * (
                data_list["chip"] + T_d - sumple)/(2 - data_list["amp_ratio"])
        else:  # 逆相
            data_list["multipath"] = -data_list["amp_ratio"] * (
                data_list["chip"] + T_d - sumple)/(2 + data_list["amp_ratio"])
        exit
    plot_list.append(data_list["multipath"])
    i += 1

print("multipath =", data_list["multipath"], "[m]")
print(plot_list)

x = np.arange(0, 1.5, 0.01)
y = plot_list
plt.xlabel("multipath delay")
plt.ylabel("multipath error")
plt.plot(x, y)
plt.show()
