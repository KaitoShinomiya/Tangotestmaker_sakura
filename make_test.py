import random


def make_test(original_list, start, end, how_many, which_lang, is_random, is_select_from_4):
    # ここから
    start = start - 1
    origin_df_len = len(original_list)
    selected_list = original_list[start:end]

    if is_random == 1:
        selected_list = random_select(selected_list, start, end, how_many)
        # return [('produce', 'を生産する'), ('include', 'を含む'),]
    else:
        selected_list = selected_list

    if is_select_from_4 == 0:
        test_df = select_from_4(selected_list, original_list, origin_df_len, which_lang)

    else:
        test_df = drop_en_or_jp(selected_list, which_lang)
        # ['involve', 'consider', 'concern', 'produce', 'create', 'allow', 'require', 'provide', 'appear', 'include']

    return test_df


def random_select(selected_list, start, end, how_many): #300-1 400 50
    random_list = range(start, end)
    random_number = random.sample(random_list, how_many)
    random_selected_list = []
    for j in range(0, how_many):  # 出題したい個数
        print(selected_list)
        print(random_number)
        print(j)
        each_list = selected_list[random_number[j] - start]
        print(each_list)
        random_selected_list.append(each_list)

    print(random_selected_list)
    print(len(random_selected_list))
    return random_selected_list


def drop_en_or_jp(selected_list, which_lang):
    if which_lang == 0:
        quiz_row = 0
        answer_row = 1
    else:
        answer_row = 0
        quiz_row = 1

    return_dict = {}
    quiz_number = 1
    for i in selected_list:
        return_dict[quiz_number] = {'question': i[quiz_row], 'answers': '       ', 'correct': i[answer_row]}
        quiz_number = quiz_number + 1
    print(return_dict)
    return return_dict


def select_from_4(selected_list, original_list, origin_df_len, which_lang):
    answer_lang_row = 1
    if which_lang == 1:  # when japanse
        selected_list_tmp = []
        for i in selected_list:
            value_taple = (i[1], i[0])
            selected_list_tmp.append(value_taple)
        selected_list = selected_list_tmp
        answer_lang_row = 0
    quiz_dict = {}
    quiz_number = 1
    for i in selected_list:
        answer_list = [i[1]]
        for j in range(0, 3):
            get_value_key = random.randint(0, origin_df_len - 1)
            answer_list.append(original_list[get_value_key][answer_lang_row])
        random.shuffle(answer_list)
        quiz_dict[quiz_number] = {'question': i[0], 'answers': answer_list, 'correct': i[1]}
        quiz_number = quiz_number + 1
    # quiz = {
    #     1: {
    #         question: 'information',
    #         answers: ['情報', '作る', '食べ物', '走る'],
    #         correct: '情報'
    #     }
    # };
    return quiz_dict
