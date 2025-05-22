import pandas as pd
import numpy as np

# 读取TSV数据
def read_tsv_data(file_path):
    return pd.read_csv(file_path, sep='\t')

# 或者从字符串读取
def read_tsv_from_string(tsv_string):
    import io
    return pd.read_csv(io.StringIO(tsv_string), sep='\t',index_col=False)

# 示例TSV字符串，可以替换为文件路径
tsv_data = """Method	model	mode	Cross CSD Score (Ref-Gen)	Self CSD Score (Gen-Gen)	Cross Cref Score (Ref-Gen)	Self Cref Score (Gen-Gen)	Aesthetics Score	Inception Score	Prompt Align (Scene)	Prompt Align (Camera)	Prompt Align (Character Existence|Number) OCCM	Prompt Align (Global Character Action|Script)	Prompt Align (Local/Single Character Action|Script)	Prompt Align Avg（Alignment score）
Story image method	Storydiffusion	Text only	0.315	0.687	0.307	0.578	5.828	12.992	3.154	2.801	0.819	1.742	1.793	59.308	
Story image method	Storydiffusion	(Img ref) (photomaker)	0.423	0.618	0.331	0.61	5.207	8.178	1.763	3.209	0.832	2.333	2.407	60.696	
Story image method	Storyadapter	(Text only) (scale0)	0.359	0.515	0.314	0.542	5.12	12.724	1.884	3.236	0.827	2.523	2.294	62.107	
Story image method	Storyadapter	(Text only) (scale5)	0.364	0.754	0.296	0.593	4.852	10.593	1.787	2.998	0.826	2.391	1.861	56.479	
Story image method	Storyadapter	(Img ref)(scale0)	0.527	0.616	0.345	0.597	4.892	11.485	1.804	3.141	0.845	2.393	2.329	60.414	
Story image method	Storyadapter	(Img ref)(scale5)	0.382	0.759	0.295	0.55	4.803	12.025	1.695	3.004	0.815	2.222	2.048	56.056	
Story image method	Storygen	(Auto-regressive)	0.407	0.558	0.376	0.588	4.091	7.152	0.974	2.165	0.836	1.21	1.299	35.302	
Story image method	Storygen	(Multi-image-condition)	0.399	0.549	0.37	0.642	4.089	7.667	1.091	2.043	0.831	1.352	1.419	36.902	
Story image method	Storygen	(Mix)	0.315	0.609	0.364	0.688	3.862	6.246	0.75	2.154	0.833	1.231	1.598	35.823	
Story image method	UNO (many2many version)	base	0.446	0.656	0.423	0.692	5.134	10.497	3.479	2.927	0.891	2.817	2.321	72.147	
Story image method	Theatergen	base	0.237	0.421	0.265	0.546	4.943	13.604	2.752	1.729	0.813	0.953	1.037	40.446	
Story image method	Seedstory(AR) 	base	0.264	0.762	0.219	0.486	3.823	4.927	1.932	1.776	0.831	0.478	0.473	29.118	
MLLM model	GPT4o	base	0.487	0.685	0.532	0.731	5.519	9.019	3.868	3.568	0.934	3.755	3.099	89.315	
MLLM model	Gemini	base	0.381	0.586	0.315	0.537	4.906	10.117	3.482	3.081	0.869	3.045	2.565	76.083	
Story video method	Vlogger	text only	0.257	0.462	0.287	0.554	4.302	8.443	1.629	2.82	0.834	2.352	2.127	55.799	
Story video method	Vlogger	img ref	0.315	0.498	0.3	0.54	4.297	9.053	1.655	2.909	0.82	2.259	2.176	56.242	
Story video method	Movieagent	ROICtrl version	0.248	0.557	0.277	0.577	4.704	10.07	1.183	2.344	0.843	1.368	1.298	38.707	
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
"""  # 这里贴入完整的TSV数据

def analyze_leaderboard(data):
    # 转换所有可能的数值列为浮点数
    metric_cols = data.columns[3:]  # 假设前3列是Method, model, mode
    for col in metric_cols:
        data[col] = pd.to_numeric(data[col], errors='coerce')
    
    # 为每个指标计算排名（默认所有指标值越高越好）
    # 如果有指标值越低越好，需要修改排名计算方式
    ranks = pd.DataFrame()
    for col in metric_cols:
        # 如果是Inception Score，值越低越好
        if 'Inception' in col:
            ranks[f"{col}_rank"] = data[col].rank(ascending=True)
        else:
            # 其他指标值越高越好
            ranks[f"{col}_rank"] = data[col].rank(ascending=False)
    
    # 计算每行的平均排名
    rank_cols = [col for col in ranks.columns if col.endswith('_rank')]
    ranks['avg_rank'] = ranks[rank_cols].mean(axis=1)
    
    # 合并原始数据和排名数据
    result = pd.concat([data, ranks], axis=1)
    
    # 添加总排名列
    result['overall_rank'] = result['avg_rank'].rank()
    
    # 分组计算不同mode的排名
    # 排除mode为'base'的记录
    filtered_result = result[result['mode'] != 'base'].copy()
    
    # 按Method和model分组
    mode_comparison = filtered_result.groupby(['Method', 'model']).apply(
        lambda group: group.sort_values('avg_rank').reset_index(drop=True)
    ).reset_index(drop=True)
    
    # 按Method和model分组，找出每组中平均排名最好的mode
    best_modes = filtered_result.loc[
        filtered_result.groupby(['Method', 'model'])['avg_rank'].idxmin()
    ][['Method', 'model', 'mode', 'avg_rank', 'overall_rank']]
    
    return {
        'detailed_ranks': result,
        'mode_comparison': mode_comparison,
        'best_modes': best_modes
    }

# 使用示例
# 如果有完整的TSV文件，可以使用：df = read_tsv_data('path/to/file.tsv')
df = read_tsv_from_string(tsv_data)
results = analyze_leaderboard(df)

# 输出所有记录的详细排名
print("排名详情:")
print(results['detailed_ranks'][['Method', 'model', 'mode', 'avg_rank', 'overall_rank']])

# 输出每个Method和model组合下最佳的mode
print("\n每个方法和模型组合下的最佳模式:")
print(results['best_modes'])