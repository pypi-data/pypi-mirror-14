"""����"gynester.py"ģ�飬�ṩ��һ����Ϊprint_lol()�ĺ���,��������������Ǵ�ӡ�б�
�����п��ܰ���(Ҳ���ܲ�����)Ƕ���б�"""
def print_lol(list_item):
    """�������ȡһ��λ�ò�������Ϊ"list_item",��������κ�Python�б�(Ҳ�����ǰ�
    ��Ƕ���б���б�)����ָ�����б��е�ÿ���������(�ݹ��)�������Ļ�ϣ�������
    ���ռһ��"""
    for each_item in list_item:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            print(each_item)
