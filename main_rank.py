import pandas as pd
import numpy as np
import io

# 读取TSV数据
def read_tsv_data(file_path):
    return pd.read_csv(file_path, sep='\t')

# 从字符串读取TSV数据
def read_tsv_from_string(tsv_string):
    return pd.read_csv(io.StringIO(tsv_string), sep='\t', index_col=False)

# TSV数据字符串
lite="""Method	model	mode	Cross CSD Score (Ref-Gen)	Self CSD Score (Gen-Gen)	Cross Cref Score (Ref-Gen)	Self Cref Score (Gen-Gen)	Aesthetics Score	Inception Score	Prompt Align (Scene)	Prompt Align (Camera)	Prompt Align (Character Existence|Number) OCCM	Prompt Align (Global Character Action|Script)	Prompt Align (Local/Single Character Action|Script)	Prompt Align Avg（Alignment score）
Story image method	Storydiffusion	(Img ref) (photomaker)	0.423	0.618	0.331	0.61	5.207	8.178	1.763	3.209	0.832	2.333	2.407	60.696	
Story image method	Storyadapter	(Img ref)(scale0)	0.527	0.616	0.345	0.597	4.892	11.485	1.804	3.141	0.845	2.393	2.329	60.414	
Story image method	Storygen	(Multi-image-condition)	0.399	0.549	0.37	0.642	4.089	7.667	1.091	2.043	0.831	1.352	1.419	36.902	
Story image method	UNO (many2many version)	base	0.446	0.656	0.423	0.692	5.134	10.497	3.479	2.927	0.891	2.817	2.321	72.147	
Story image method	Theatergen	base	0.237	0.421	0.265	0.546	4.943	13.604	2.752	1.729	0.813	0.953	1.037	40.446	
Story image method	Seedstory(AR) 	base	0.264	0.762	0.219	0.486	3.823	4.927	1.932	1.776	0.831	0.478	0.473	29.118	
MLLM model	GPT4o	base	0.487	0.685	0.532	0.731	5.519	9.019	3.868	3.568	0.934	3.755	3.099	89.315	
MLLM model	Gemini	base	0.381	0.586	0.315	0.537	4.906	10.117	3.482	3.081	0.869	3.045	2.565	76.083	
Story video method	Vlogger	text only	0.257	0.462	0.287	0.554	4.302	8.443	1.629	2.82	0.834	2.352	2.127	55.799	
Story video method	Movieagent	SD-3 version	0.361	0.543	0.357	0.605	5.332	12.049	3.365	2.905	0.869	3.282	2.648	76.257	
Story video method	Animdirector	base	0.321	0.555	0.384	0.655	5.612	9.996	3.634	2.734	0.877	3.35	2.546	76.651	
Story video method	MM-StoryAgent	base	0.28	0.662	0.321	0.566	5.91	8.088	2.888	2.295	0.822	1.493	1.39	50.419	
Business platform	moki	base	0.229	0.7	0.292	0.626	5.813	10.358	2.81	1.668	0.82	0.888	0.848	38.841	
Business platform	morphic_studio	base	0.59	0.638	0.5	0.664	4.956	9.004	3.278	2.934	0.829	2.475	2.106	67.46	
Business platform	bairimeng_ai	base	0.426	0.73	0.559	0.762	5.731	9.552	3.447	2.789	0.894	2.361	1.83	65.172	
Business platform	shenbimaliang	base	0.292	0.582	0.347	0.611	5.07	11.599	3.742	2.66	0.856	3.37	2.358	75.809	
Business platform	xunfeihuiying	base	0.342	0.652	0.392	0.546	5.321	11.156	2.773	2.708	0.841	2.424	2.081	62.421	
Business platform	doubao	base	0.386	0.698	0.394	0.714	5.615	9.878	3.96	2.995	0.875	3.721	2.788	84.155	
Naive baseline	base	base	0.736	0.773	0.932	0.996	4.396	5.474	0.532	2.021	1	0.671	1.097	27.003	
"""
full="""Method	model	mode	Cross CSD Score (Ref-Gen)	Self CSD Score (Gen-Gen)	Cross Cref Score (Ref-Gen)	Self Cref Score (Gen-Gen)	Aesthetics Score	Inception Score	Prompt Align (Scene)	Prompt Align (Camera)	Prompt Align (Character Existence|Number)	Prompt Align (Global Character Action|Script)	Prompt Align (Local/Single Character Action|Script)	Prompt Align Avg
Story image method	Storydiffusion	(Img ref) (photomaker)	0.3511	0.5536	0.3379	0.6634	5.125	10.057	1.878	3.266	0.868	2.411	2.23	61.151	
Story image method	Storyadapter	(Img ref)(scale0)	0.4619	0.5537	0.3533	0.6653	4.995	12.978	1.953	3.263	0.857	2.489	2.25	62.218	
Story image method	Storygen	Multi-image-condition	0.3711	0.5256	0.3518	0.6399	4.022	8.889	1.123	2.125	0.862	1.304	1.387	37.117	
Story image method	UNO (many2many version)	base	0.408	0.6103	0.3938	0.6711	5.232	12.398	3.47	3.062	0.898	2.617	2.121	70.43	
Story image method	Theatergen	base	0.1989	0.4037	0.2708	0.6045	4.897	14.882	2.673	1.645	0.844	0.874	0.875	37.923	
Story image method	Seedstory(AR) 	base	0.2334	0.7486	0.2174	0.5286	3.836	6.325	1.931	1.638	0.859	0.592	0.559	29.499	
Story video method	Vlogger	text only	0.2141	0.4073	0.2686	0.5662	4.334	10.482	1.576	2.854	0.845	2.191	1.982	53.769	
Story video method	Movieagent	SD-3 version	0.3089	0.4826	0.3163	0.607	5.33	15.021	3.456	2.985	0.875	3.233	2.496	76.061	
Story video method	Animdirector	base	0.2983	0.507	0.3388	0.6534	5.599	12.037	3.607	2.887	0.884	3.239	2.435	76.049	
Story video method	MM-StoryAgent	base	0.2528	0.6677	0.3132	0.6459	5.883	9.093	2.832	2.459	0.852	1.688	1.358	52.106	
Naive baseline	base	base	0.7279	0.7154	0.9406	0.9866	4.477	6.719	0.486	2.06	0.997	0.655	0.99	26.197	
"""
def analyze_dimensions(data):
    # 转换所有可能的数值列为浮点数
    metric_cols = data.columns[3:]
    for col in metric_cols:
        data[col] = pd.to_numeric(data[col], errors='coerce')
    
    # 定义五个评估维度及其包含的指标
    dimensions = {
        "Character Consistency(CRef)": [
            "Cross Cref Score (Ref-Gen)", 
            "Self Cref Score (Gen-Gen)"
        ],
        "Style Consistency(SRef)": [
            "Cross CSD Score (Ref-Gen)", 
            "Self CSD Score (Gen-Gen)"
        ],
        "Prompt Alignment": [
            "Prompt Align (Scene)",
            "Prompt Align (Camera)",
            "Prompt Align (Character Existence|Number) OCCM",
            "Prompt Align (Global Character Action|Script)",
            "Prompt Align (Local/Single Character Action|Script)",
            "Prompt Align Avg（Alignment score）"
        ],
        "Generative Quality": [
            "Aesthetics Score"
        ],
        "Diversity": [
            "Inception Score"
        ]
    }
    
    # 计算每个维度中各指标的排名
    dimension_ranks = {}
    for dim_name, metrics in dimensions.items():
        dim_df = pd.DataFrame()
        for metric in metrics:
            if metric in data.columns:

                    # 其他指标值越高越好
                    dim_df[f"{metric}_rank"] = data[metric].rank(ascending=False)
        
        # 如果该维度有有效指标
        if not dim_df.empty:
            # 计算维度的平均排名
            rank_cols = dim_df.columns
            dim_df[f"{dim_name}_avg_rank"] = dim_df[rank_cols].mean(axis=1)
            dimension_ranks[dim_name] = dim_df[f"{dim_name}_avg_rank"]
    
    # 合并所有维度的排名
    for dim_name, ranks in dimension_ranks.items():
        data[f"{dim_name}_avg_rank"] = ranks
        data[f"{dim_name}_rank"] = ranks.rank()
    
    # 计算全部维度的综合排名
    avg_rank_cols = [col for col in data.columns if col.endswith('_avg_rank')]
    data['overall_avg_rank'] = data[avg_rank_cols].mean(axis=1)
    data['overall_rank'] = data['overall_avg_rank'].rank()
    
    # 创建一个简洁的结果数据框
    result_cols = ['Method', 'model', 'mode']
    for dim_name in dimensions.keys():
        result_cols.append(f"{dim_name}_rank")
    result_cols.append('overall_rank')
    
    result_df = data[result_cols].copy()
    
    # 创建方法-模型的唯一标识符，用于按模型分组
    result_df['model_key'] = result_df['Method'] + ' - ' + result_df['model']
    
    # 为每个模型找出最佳模式
    best_modes = result_df.loc[
        result_df.groupby(['model_key'])['overall_rank'].idxmin()
    ].sort_values('overall_rank')
    
    return {
        'all_rankings': result_df,
        'best_modes': best_modes
    }

# 从TSV字符串读取数据
df = read_tsv_from_string(full)
results = analyze_dimensions(df)

# 输出每个方法-模型在各维度的排名详情
print("各模型在不同维度的排名:")
rankings_display = results['all_rankings'].sort_values('overall_rank')
print(rankings_display)

# 输出每个方法-模型的最佳模式
# print("\n每个模型的最佳模式:")
# best_modes_display = results['best_modes'][['Method', 'model', 'mode', 'overall_rank']]
# print(best_modes_display)

# # 将结果保存为CSV文件
rankings_display.to_csv('full.csv', index=False)
# best_modes_display.to_csv('best_modes.csv', index=False)

# print("\n结果已保存至 dimension_rankings.csv 和 best_modes.csv")
df=read_tsv_from_string(lite)
results=analyze_dimensions(df)
rankings_display=results['all_rankings'].sort_values('overall_rank')
rankings_display.to_csv('lite.csv', index=False)