from utils.getPublicData import getAllCasesData


def getPieData():
    casesList = getAllCasesData()
    ageDic = {'0-10岁':0,'10-20岁':0,'10-20岁':0,'20-30岁':0,'30-40岁':0,'40-50岁':0,'50-60岁':0,'60岁以上':0}
    for caseItem in casesList:
        if int(caseItem['age']) < 10:
            ageDic['0-10岁'] += 1
        elif int(caseItem['age']) < 20:
            ageDic['10-20岁'] += 1
        elif int(caseItem['age']) < 30:
            ageDic['20-30岁'] += 1
        elif int(caseItem['age']) < 40:
            ageDic['30-40岁'] += 1
        elif int(caseItem['age']) < 50:
            ageDic['40-50岁'] += 1
        elif int(caseItem['age']) < 60:
            ageDic['50-60岁'] += 1
        else:
            ageDic['60岁以上'] += 1
    # print(ageDic)
    listResult = []
    for k,v in ageDic.items():
        listResult.append({
            'name':k,
            'value':v
        })
    print(listResult)
    return listResult

def getConfigOne():
    casesList = getAllCasesData()
    caseDic = {}
    for caseItem in casesList:
        # 兼容孕产妇数据和普通病例数据
        disease_field = caseItem.get('disease') or caseItem.get('pregnancy_status', '未知')
        if caseDic.get(disease_field, -1) == -1:
            caseDic[disease_field] = 1
        else:
            caseDic[disease_field] += 1
    listResult = []
    for k, v in caseDic.items():
        listResult.append({
            'name': k,
            'value': v
        })
    print(1, listResult)
    return listResult[:6], listResult

def getFoundData():
    casesList = getAllCasesData()
    maxNum = len(list(casesList))
    typeDic = {}
    depDic = {}
    hosDic = {}
    maxAge = 0
    minAge = 100
    for caseItem in casesList:
        # 兼容孕产妇数据和普通病例数据
        disease_field = caseItem.get('disease') or caseItem.get('pregnancy_status', '未知')
        department_field = caseItem.get('department', '未知')
        hospital_field = caseItem.get('hospital', '未知')
        age_field = int(caseItem.get('age', 0))
        
        #类型
        if typeDic.get(disease_field, -1) == -1:
            typeDic[disease_field] = 1
        else:
            typeDic[disease_field] += 1
        #科室
        if depDic.get(department_field, -1) == -1:
            depDic[department_field] = 1
        else:
            depDic[department_field] += 1
        #医院
        if hosDic.get(hospital_field, -1) == -1:
            hosDic[hospital_field] = 1
        else:
            hosDic[hospital_field] += 1
        #年龄
        if age_field > maxAge:
            maxAge = age_field
        if age_field < minAge:
            minAge = age_field

    typeSort = sorted(typeDic.items(), key=lambda data: data[1], reverse=True)
    depSort = sorted(depDic.items(), key=lambda data: data[1], reverse=True)
    hosSort = sorted(hosDic.items(), key=lambda data: data[1], reverse=True)
    
    # 添加错误处理，确保即使列表为空也能正常运行
    maxType = typeSort[0][0] if typeSort else "未知"
    maxDep = depSort[0][0] if depSort else "未知"
    maxHos = hosSort[0][0] if hosSort else "未知"
    
    return maxNum, maxType, maxDep, maxHos, maxAge, minAge

def getGenderData():
    casesList = getAllCasesData()
    boyDic = {}
    girlDic = {}
    boyNum = 0
    girlNum = 0
    for caseItem in casesList:
        gender_field = caseItem.get('gender', '女')  # 孕产妇默认为女性
        # 兼容孕产妇数据和普通病例数据
        disease_field = caseItem.get('disease') or caseItem.get('pregnancy_status', '未知')
        
        if gender_field == '男':
            boyNum += 1
            if boyDic.get(disease_field, -1) == -1:
                boyDic[disease_field] = 1
            else:
                boyDic[disease_field] += 1
        elif gender_field == '女':
            girlNum += 1
            if girlDic.get(disease_field, -1) == -1:
                girlDic[disease_field] = 1
            else:
                girlDic[disease_field] += 1

    ratioData = []
    # 添加除以零检查，确保即使casesList为空也能正常运行
    totalCases = len(casesList)
    if totalCases == 0:
        boyRatio = 0
        girlRatio = 0
    else:
        boyRatio = int(round(boyNum / totalCases * 100, 0))
        girlRatio = int(round(girlNum / totalCases * 100, 0))
    print(boyRatio, girlRatio)
    ratioData.append(girlRatio)
    ratioData.append(boyRatio)
    boyList = []
    girlList = []
    for k, v in boyDic.items():
        boyList.append({
            'name': k,
            'value': v
        })
    for k, v in girlDic.items():
        girlList.append({
            'name': k,
            'value': v
        })
    return boyList, girlList, ratioData

def getCircleData():
    casesList = getAllCasesData()
    depDic = {}
    for caseItem in casesList:
        department_field = caseItem.get('department', '未知')
        if depDic.get(department_field, -1) == -1:
            depDic[department_field] = 1
        else:
            depDic[department_field] += 1
    # print(depDic)
    dataSort = sorted(depDic.items(), key=lambda data: data[1], reverse=True)
    dataResultList = []
    for i in dataSort:
        dataResultList.append({
            'name': i[0],
            'value': i[1]
        })

    return dataResultList

def getBodyData():
    # 由于数据库表结构中没有字段10和11，暂时返回空数据以避免错误
    # 修复disease字段的访问
    casesList = getAllCasesData()
    dataDic = {}
    xData = []
    sumData = []
    for caseItem in casesList:
        # 兼容孕产妇数据和普通病例数据
        disease_field = caseItem.get('disease') or caseItem.get('pregnancy_status', '未知')
        if dataDic.get(disease_field, -1) == -1:
            dataDic[disease_field] = 1
        else:
            dataDic[disease_field] += 1
    dataSort = sorted(dataDic.items(), key=lambda data: data[1], reverse=True)
    for i in dataSort:
        xData.append(i[0])
        sumData.append(i[1])
    # 暂时返回空数据，因为数据库中没有字段10和11
    y1Data = [0 for x in range(len(xData))]
    y2Data = [0 for x in range(len(xData))]
    return xData, y1Data, y2Data
