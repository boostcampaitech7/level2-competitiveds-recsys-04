# 🏠 수도권 아파트 전세가 예측 모델

## 📌 프로젝트 개요
본 프로젝트는 수도권 아파트 전세 실거래가를 예측하는 모델을 개발하는 것을 목표로 했습니다.  
시계열 데이터 분석, 머신러닝 모델링 등 다양한 기술을 실제 문제에 적용하여, 예측하는 것이 주요 과제였습니다.
## 📊 프로젝트 데이터
제공된 데이터셋은 아파트 전세 실거래가 예측을 목표로 하며, 학습 데이터와 테스트 데이터에는 각 건물의 기본적인 정보와 전세 실거래가로 구성됩니다.  
또한 지하철, 공원, 학교, 금리 데이터가 추가적으로 제공됩니다.

- **학습 데이터**: 2019년 4월 1일 ~ 2023년 12월 31일 (1,801,228개)
- **평가 데이터**: 2024년 1월 1일 ~ 2024년 6월 20일 (150,172개)
- **금리 데이터**: 2018년 12월 ~ 2024년 7월 (68개)
- **공원 데이터**: 위도, 경도, 면적 (17,564개)
- **학교 데이터**: 위도, 경도 (11,992개)
- **지하철 데이터**: 위도, 경도 (700개)
## 🗂️ 파일 구조
```
.
├── README.md
├── config
│   ├── cluster_dedep.pkl
│   ├── index_list.pkl 
│   ├── lgbm_params.yaml
│   ├── raddi_values.yaml
│   ├── raddi_values_lgbm.yaml
│   └── xgb_params_info.pkl
├── data
│   ├──
│   └──
├── results
│   ├── xgb_deposit_per_area.csv
│   ├── xgb_deposit.csv
│   ├── lgbm.csv
│   └── esemble.csv
├── utils
│   ├──age_group.py
│   ├──compute_place_metrics.py
│   ├──config_loader.py
│   ├──HuberLoss.py
│   ├──age_group.py 
│   └──
├── feature-extraction.py
└── src
    ├── ensemble.py
    └── models
        ├── lgbm.py
        ├── xgb_depoist.py
        └── xgb_deposit_per_area.py
```

### 폴더 및 파일 설명
- **config 폴더**
 raddi_values_lgbm.yaml 은 lgbm.py 에 들어가는 데이터를 만들기 위한 파일입니다.
 raddi_values.yaml 은 xgb_depoist.py, xgb_deposit_per_area.py 에 들어가는 데이터를 만들기 위한 파일입니다.
index_list.pkl, cluster_dedep.pkl, xgb_params_info.pkl 파일들은 xgb_deposit_per_area.py 를 실행할 때 사용하는 파일들 입니다.
ensemble.yaml 은 esemble.py 를 실행할 때 사용하는 YAML 파일입니다. 앙상블하고 싶은 CSV 파일과 각 모델에 할당할 가중치가 적혀 있습니다.

- **data 폴더**  


- **results 폴더**
 이 폴더에는 각 모델이 예측한 결과 파일들이 저장됩니다. 각 CSV 파일은 모델별로 다르게 생성되며, 이를 바탕으로 최종 앙상블 결과를 도출합니다.
 xgb_deposit_per_area.csv, xgb_deposit.csv, lgbm.csv : 각 모델의 예측 결과가 저장된 파일들입니다.
 esemble.csv : 모델의 예측 결과로 앙상블 한 파일입니다.


- **src 폴더**
  이 폴더에는 프로젝트의 핵심 Python 코드가 포함되어 있습니다.

 * ensemble.py: 여러 모델의 예측 결과를 soft voting 방식으로 앙상블해주는 코드입니다. YAML 파일을 읽어와 가중치와 함께 예측을 진행합니다.

 * models 폴더: 각종 머신러닝 모델들이 구현된 파일들이 들어 있습니다.

    lgbm.py: LightGBM 바탕으로 만든 모델입니다. 세부 내용은 #2 PR에서 확인할 수 있습니다.

    xgb_deposit_per_area.py: XGBoost를 바탕으로 만든 모델입니다. 자세한 내용은 #3 PR을 참고하세요.

    xgb_deposit.py: XGBoost 기반 모델로, 자세한 내용은 #6 PR에서 확인할 수 있습니다.

## 🛠️ 사용 방법
1. **개별 모델 실행:**  
   `src` 폴더에 존재하는 `feature-extraction`을 실행하면 모델 실행을 위한 데이터 파일(`train_aftercountplace.csv`, `test_aftercountplace.csv`)이 생성됩니다.
   
   실행 시, `config` 폴더에 있는 적용할 `radii_values` YAML 파일을 입력으로 제공해야 합니다.

    ```
    python feature-extraction.py radii_values.yaml
    ```

    이후 `src/models` 폴더에 
2. **앙상블(Ensemble) 실행:**  
    `src/ensemble.py`는 각 모델이 예측한 `csv` 파일을 읽어 soft voting 방식으로 앙상블을 진행합니다.  

    앙상블 실행 시, `config` 폴더에 있는 YAML 파일을 입력으로 제공해야 하며, 해당 YAML 파일은 예측에 사용될 CSV 파일과 각 파일의 가중치를 정의합니다.  

    ```
    python ensemble.py yaml_file_name.yaml
    ```

    
## 🎯 파이널 제출 내역


## 😊 팀 구성원
<div align="center">
<table>
  <tr>
    <td align="center"><a href="https://github.com/Heukma"><img src="https://avatars.githubusercontent.com/u/77618270?v=4" width="100px;" alt=""/><br /><sub><b>성효제</b></sub><br />
    </td>
        <td align="center"><a href="https://github.com/gagoory7"><img src="https://avatars.githubusercontent.com/u/163074222?v=4" width="100px;" alt=""/><br /><sub><b>백상민</b></sub><br />
    </td>
        <td align="center"><a href="https://github.com/Timeisfast"><img src="https://avatars.githubusercontent.com/u/120894109?v=4" width="100px;" alt=""/><br /><sub><b>김성윤</b></sub><br />
    </td>
        <td align="center"><a href="https://github.com/annakong23"><img src="https://avatars.githubusercontent.com/u/102771961?v=4" width="100px;" alt=""/><br /><sub><b>공지원</b></sub><br />
    </td>
        <td align="center"><a href="https://github.com/kimjueun028"><img src="https://avatars.githubusercontent.com/u/92249116?v=4" width="100px;" alt=""/><br /><sub><b>김주은</b></sub><br />
    </td>
    </td>
        <td align="center"><a href="https://github.com/zip-sa"><img src="https://avatars.githubusercontent.com/u/49730616?v=4" width="100px;" alt=""/><br /><sub><b>박승우</b></sub><br />
    </td>
  </tr>
</table>
</div>

<br />
