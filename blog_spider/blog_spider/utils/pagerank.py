import numpy as np
import json
def compute_pagerank(nodes, alpha=0.85, iterations=100):
    # 构建URL到ID的映射
    url_to_id = {node['url']: i for i, node in enumerate(nodes)}
    n = len(nodes)

    # 构建初始链接矩阵
    M = np.zeros((n, n))
    for node in nodes:
        node_id = url_to_id[node['url']]
        out_links = node['relate']
        if not out_links:
            # 如果没有外链，认为它链接到所有页面
            M[:, node_id] = 1 / n
        else:
            for link in out_links:
                if link in url_to_id:  # 只考虑列表中的链接
                    linked_node_id = url_to_id[link]
                    M[linked_node_id, node_id] = 1 / len(out_links)

    # 计算PageRank
    teleport = np.ones(n) / n
    r = np.ones(n) / n
    for _ in range(iterations):
        r = alpha * M @ r + (1 - alpha) * teleport

    # 更新节点的PageRank值
    for node in nodes:
        node_id = url_to_id[node['url']]
        node['PR'] = r[node_id]

    return nodes

json_file_path = '/Users/liuvivian/Blog_Search_Engine/blog_spider/blog_spider/spiders/output1.json'

# 读取JSON文件并将内容加载到变量中
try:
    with open(json_file_path, 'r', encoding='utf-8') as file:
        nodes = json.load(file)
    print(nodes[:2])  # 打印前两个节点，作为示例
except FileNotFoundError:
    print(f"文件未找到: {json_file_path}")
except json.JSONDecodeError:
    print(f"JSON文件解析错误: {json_file_path}")


# 计算PageRank值
pageranked_nodes = compute_pagerank(nodes)

# 将计算后的节点数据保存回JSON文件
json_output_path = '/Users/liuvivian/Blog_Search_Engine/blog_spider/finaloutput.json'  # 替换为输出JSON文件的实际路径
with open(json_output_path, 'w', encoding='utf-8') as file:
    json.dump(pageranked_nodes, file, ensure_ascii=False, indent=4)

# 打印结果
for node in pageranked_nodes:
    print(f"URL: {node['url']}, PageRank: {node['PR']}")
