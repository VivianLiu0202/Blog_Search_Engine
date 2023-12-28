import numpy as np
from lightfm import LightFM
from lightfm.data import Dataset
from searchblog.models import CustomUser, SearchQueryLog, ClickLog
from elasticsearch_dsl import Search
from django.conf import settings
from searchblog.views import get_all_links_from_es,get_top_queries,get_user_interactions
from django.contrib.auth import get_user_model
import pickle
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Train the recommendation model'
    def handle(self, *args, **kwargs):
        def build_interaction_matrix(users, links, logs):
            """
            构建用户-链接交互矩阵
            :param users: 用户列表
            :param links: 链接列表
            :param logs: 用户查询日志，形如[(user_id, link_id), ...]
            :return: 交互矩阵，用户和链接的特征映射
            """
            dataset = Dataset()
            dataset.fit(users, links)
            
            # 构建交互数据
            (interactions, weights) = dataset.build_interactions(logs)
            
            return interactions, dataset.mapping()

        def train_model(interactions):
            """
            训练隐语义模型
            :param interactions: 用户-链接交互矩阵
            :return: 训练好的模型
            """
            # 使用WARP损失函数的LightFM模型
            model = LightFM(loss='warp')
            model.fit(interactions, epochs=30, num_threads=2)
            
            return model

        # 获取所有用户和链接
        User = get_user_model()
        users = User.objects.all().values_list('id', flat=True)
        links = get_all_links_from_es()
        print('users',users)

        # 获取用户点击日志
        logs = get_user_interactions()
        print('logs',logs)

        # 构建交互矩阵
        interactions, mapping = build_interaction_matrix(users, links, logs)

        # 训练模型
        model = train_model(interactions)

        # 保存模型和映射
        with open('recommendation_model.pkl', 'wb') as f:
            pickle.dump(model, f)
        with open('mapping.pkl', 'wb') as f:
            pickle.dump(mapping, f)
