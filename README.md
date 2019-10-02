# MD_analysis_cpptraj
How to analyze MD trajectories using CPPTRAJ

## Prerequsitories
필요한 것:
Amber 프로그램 suite - 그 중에서 이 tutorial 에서는 cpptraj 프로그램을 사용하는 법을 다룰 예정입니다. 

LCBC 학생들은 master의 /opt/amber18/에 설치되어 있는 Amber를 사용하면 됩니다. 
MD trajectory files. (*.nc or *.mdcrd)
Parameter files. (*.prmtop)

## Quick start
아래에 있는 script는 cpptraj 프로그램을 이용해서 MD trajectory에서 RMSD, hydrogen-bond, 그리고 lifetime 분석을 수행하는 script입니다.
전체 파일은 같은 repository에 업로드 되어 있습니다.  

본 script를 하나씩 따라가면서 어떻게 분석이 수행되는지 살펴봅시다.
*rmsd_and_hbond_analysis.in*

### parameter 파일 지정하기 
parm 명령어를 이용해서 일단 parameter 파일을 지정해줍니다. 

```
# Set up parameter & topology files.
parm msdx-rf-l1-solv.prmtop
```

### Trajectory 파일 지정하기
그 뒤에 trajin 명령을 이용해서 분석하고자 하는 대상 trajectory 파일을 지정해줍니다. 
```
trajin step5_100.nc 1 last 1
trajin step5_101.nc 1 last 1
trajin step5_102.nc 1 last 1
...
```

위의 예시에서는 세개의 파일만 저정하였지만 실제로 내가 가진 trajectory파일이 더 많다면 차례대로 다음 줄에 지정해주면 됩니다.
그리고 각 trajectory파일 뒤에 있는 option은 **첫번째 숫자는 시작하는 frame**, **두 번째는 끝나는 frame을 지정하는 부분인데 숫자 또는 *last* 를 줄 수 있습니다.**
**세번째 숫자는 *offset*에 해당하는 숫자로 몇 frame씩 뛰어 넘어서 분석할지를 지정해줍니다.**
현재 위의 예제에서는 모든 frame을 분석하도록 지정하였습니다.

만약, 내가 모든 frame을 분석하는데 시간이 너무 많이 걸리거나 메모리가 모자라서 일부분의 데이터만 쓰고 싶다면, 다음과 같이 변형시켜 줍시다.
아래 예제의 script는 매 10 번째 frame을 분석합니다. 즉, 전체 데이터의 10%만 사용해서 분석하게 되는 것입니다. 

```
trajin step5_100.nc 1 last 10
trajin step5_101.nc 1 last 10
trajin step5_102.nc 1 last 10
...
```

### Centering atoms 
일반적으로 MD simulation을 수행하면 periodic boundary condition 때문에 residue가 이상하게 위치하고 있는 경우가 많습니다.

이럴 때, autoimage는 trajectory를 보기 좋게 다시 정렬해주는 명령어입니다. 
```
autoimage
```

### RMSD 계산
RMSD 는 Root Mean Squared Deviation의 줄임말로써, 평균적으로 분자를 이루고 있는 원자들이 기준이 되는 구조와 비교하였을 때, 몇 A정도 변화하였는지를 나타내는 값입니다. 
아래는 cpptraj에서 RMSD를 계산하는 명령어입니다. 

```
rms ToFirstHeavy :1-148&!@H=    first out ToFirst_heavy.rms.txt mass
```

첫번째, rms 명령어는 rmsd 계산을 수행하겠다는 뜻입니다. 
두번째인 ToFirstHeavy는 계산된 rmsd 값이 들어있는 dataset 의 이름을 의미합니다. 이 데이터셋은 나중에 다른 계산을 위해서 불러올 수 있기 때문에 이름을 지정해주게 됩니다.

그 뒤에 어떤 atom을 이용해서 RMSD를 계산해줄지 지정해 주게 됩니다. :1-148은 1번에서 148번까지 residue를 이용하겠다는 뜻입니다. 그 뒤에 있는 !@H=은 이름이 H로 시작하는 모든 atom (@H=)이 아닌 atom들 (!이 not의 의미를 가집니다.), 다시 말해서 모든 heavy atom을 고려하겠다는 뜻입니다. 이 두가지가 and로 결합되어 있다고 생각하면 결국, 1번에서 148번 residue에 포함되어 있는 모든 heavy atom을 이용해서 RMSD를 계산하겠다는 뜻입니다. 

네 번째에 있는 *first* option은 첫번째 frame을 기준으로 RMSD를 계산하겠다는 뜻입니다. 

다섯번째 *out* option 다음에는 RMSD 값을 출력하는 결과 파일의 이름이 오게 됩니다. 

마지막의 mass는 rmsd를 계산할 때, atomic mass를 고려해서 계산하겠다는 뜻입니다. 무거운 원소의 변화가 RMSD 계산에서 더 많이 반영되도록 하는 것입니다.

만약, backbone에 있는 atom만의 rmsd를 계산하겠다면 다음과 같은 line을 사용하면 됩니다. 

```
rms  ToFirstBB  :1-148&@C,CA,N  first  out  ToFirst_backbone.rms.txt  mass
```

### Hydrogen bond analysis

단백질을 비롯한 biological molecule의 경우 수소 결합이 그 구조와 기능을 조절하는데 중요한 역할을 한다는 것이 잘 알려져있습니다.
그렇기 때문에 어떠한 수소결합이 얼마나 많이 생성되는지를 분석하는 것은 매우 의미있는 분석 방법입니다.
Cpptraj에서는 매우 강력한 수소 결합 분석 기능을 제공합니다. 
다음 예제는 수소 결합 계산을 수행하는 예시입니다. 

```
hbond  HB    out HB.hbvtime.dat \
       solventdonor :WAT solventacceptor :WAT@O \
       avgout    HB.UU.avg.dat \
       solvout   HB.UV.avg.dat \
       bridgeout HB.bridge.avg.dat \
       series uuseries uuhbonds.agr uvseries uvhbonds.agr 
```

위 예제에서 hbond 명령은 수소 결합을 수행하겠다는 뜻입니다. 그 뒤에 따라오는 HB는 수소 결합 분석 결과가 저장되는 데이터셋의 이름이 됩니다. 
HB 데이터셋에 저장된 내용은 추후에 추가적인 계산에 사용될 수 있습니다. 

*out* option 다음에 output 파일의 이름을 써줍니다.
하지만 raw 파일인 *HB.hbvtime.dat* 파일은 일반적으로 파일의 크기도 크고, 대부분의 내용이 atom number로만 표시되어 한 눈에 알아보기가 힘듭니다. 
그렇기 때문에 그 뒤에 추가적인 option이 주어지게 됩니다.

solventdonor와 solventacceptor는 각각 solvent에 존재하는 수소 결합 주개와 받개를 지정해주게 됩니다. 물이 아닌 다른 유기 용매가 사용되었다면 그에 맞게 수정이 필요합니다. 이번 예제에서는 solvent가 물이기 때문에 위와 같이 주어졌습니다. 

그 뒤에 따라오는 *avgout* 옵션은 solute안에서 생성되는 수소 결합 (solute-solute hydrogen bond) 의 평균 값을 표시하게 됩니다.
예시 결과는 다음과 같습니다. 
```
#Acceptor                DonorH           Donor   Frames         Frac      AvgDist       AvgAng
DA_12@OP1            THR_94@HG1      THR_94@OG1   390506       0.9738       2.6692     164.5806
LEU_63@O             THR_67@HG1      THR_67@OG1   371313       0.9260       2.7405     164.8568
DC_26@O2               DG_9@H21         DG_9@N2   369902       0.9224       2.8203     164.9798
DC_7@O2               DG_28@H21        DG_28@N2   358849       0.8949       2.8292     163.8071
DC_33@O2               DG_2@H21         DG_2@N2   357010       0.8903       2.8288     163.9903
DC_20@O2              DG_15@H21        DG_15@N2   355666       0.8869       2.8313     163.5028
DC_30@O2               DG_5@H21         DG_5@N2   352488       0.8790       2.8316     163.2947
DC_3@O2               DG_32@H21        DG_32@N2   341450       0.8515       2.8394     162.8517
DC_16@O2              DG_19@H21        DG_19@N2   339254       0.8460       2.8387     163.4302
```

위의 결과는 DNA와 단백질이 결합되어 있는 system의 계산 결과를 보여주고 있습니다. 
첫번째 줄을 살펴보면, 12번 DA(adenosine) residue의 OP1 atom과 94번 THR residue의 HG1 atom이 수소결합을 이루고 있다는 것을 표시합니다. 
Donor는 Thr의 HG1 atom이 붙어 있는 heavy atom을 표시합니다.

그 뒤에 있는 Frame 열은 전체 trajectory에서 몇 번의 frame 에서 해당하는 수소 결합이 관찰되었는지를 보여줍니다. 
위 예제에서는 약 39만번의 snapshot에서 수소 결합이 관찰되었다는 것을 나타냅니다.

Frac열은 전체 trajectory중에서 해당 수소 결합이 관찰된 fraction을 나타냅니다. 
전체 trajectory에서 약 97%이상에서 첫번째 line에 해당하는 수소 결합이 관찰된다는 뜻입니다. 
참고로, 위 예제에서 전체 trajectory의 frame 개수는 약 40만개 입니다. 
그러므로 simulation이 진행되는 거의 대부분의 시간 동안 첫번째 수소 결합은 유지되고 있다는 것을 알 수 있습니다. 

마지막 2열은 평균 수소 결합의 길이와 각도를 보여주고 있습니다. 

