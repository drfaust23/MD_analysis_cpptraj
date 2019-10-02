# MD_analysis_cpptraj
How to analyze MD trajectories using CPPTRAJ

## Prerequsitories
필요한 것:
Amber 프로그램 suite - 그 중에서 이 tutorial 에서는 cpptraj 프로그램을 사용하는 법을 다룰 예정입니다. 
LCBC 학생들은 master의 /opt/amber18/에 설치되어 있는 Amber를 사용하면 됩니다. 
MD trajectory files. (*.nc or *.mdcrd)
Parameter files. (*.prmtop)

## Quick start
아래에 있는 script는 cpptraj 프로그램을 이용해서 MD trajectory에서 RMSD, hydrogen-bond, 그리고 lifetime 분석을 script입니다. 
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
그리고 각 trajectory파일 뒤에 있는 option은 첫번째 숫자는 시작하는 frame, 두 번째는 끝나는 frame의 숫자 또는 *last* 를 줄 수 있습니다
세번째 숫자는 *offset*에 해당하는 숫자로 몇 frame씩 뛰어 넘어서 분석할지를 지정해줍니다. 
현재 위의 예제에서는 모든 frame을 분석하도록 지정하였습니다.

만약, 내가 모든 frame을 분석하는데 시간이 너무 많이 걸리거나 메모리가 모자라서 일부분의 데이터만 쓰고 싶다면, 다음과 같이 변형시켜 줍시다.
아래 예제의 script는 매 10 번째 frame을 분석합니다. 즉, 전체 데이터의 10%만 사용해서 분석하게 되는 것입니다. 

```
trajin step5_100.nc 1 last 10
trajin step5_101.nc 1 last 10
trajin step5_102.nc 1 last 10
...
```

