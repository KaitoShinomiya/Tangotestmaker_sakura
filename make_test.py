import random
import json
from bs4 import BeautifulSoup


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


def random_select(selected_list, start, end, how_many):
    random_list = range(start, end)
    random_number = random.sample(random_list, how_many)
    random_selected_list = []
    for j in range(0, how_many):  # 出題したい個数
        random_selected_list.append(selected_list[random_number[j]])

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
    #     }, 2: {
    #         question: 'eat',
    #         answers: ['食べる', '作る', '走る', '遊ぶ'],
    #         correct: '食べる'
    #     }
    # };
    return quiz_dict


def make_json(test, df, how_many):
    return_dict = {}
    for i in range(how_many):
        temp_dict = {}
        temp_dict['question'] = test.iloc[i, 0]
        temp_list = test.iloc[i, 1]
        temp_list = temp_list.split('・')
        for j in range(0, 4):
            temp_list[j] = temp_list[j].replace('(' + str(j + 1) + ') ', '')
            temp_list[j] = temp_list[j].replace(' ', '')
        temp_dict['answers'] = temp_list
        temp_dict['correct'] = df.iloc[i, 1]
        return_dict[i + 1] = temp_dict
    return_json = json.dumps(return_dict, ensure_ascii=False)

    return return_json


def writer_html(test, df):
    test.to_html("./tangotest_question.html", encoding='utf_8_sig',
                 classes=["table", "table-bordered", "table-hover", "col-md-8", "col-lg-8", "col-xl-8"])
    df.to_html("./tangotest_kaitou.html", encoding='utf_8_sig',
               classes=["table", "table-bordered", "table-hover", "pagebreak"])

    html_path_list = ["./tangotest_question.html", "tangotest_kaitou.html"]
    soup_list = []
    for html_path in html_path_list:
        with open(html_path) as f:
            temp = BeautifulSoup(f.read(), 'lxml')
            soup_list.append(temp)
    pure_bound_html = ''.join([soup.prettify() for soup in soup_list])
    bound_html = pure_bound_html.replace('</html>', '')
    bound_html = bound_html.replace('<html>', '')
    bound_html = bound_html.replace('<body>', '')
    bound_html = bound_html.replace('</body>', '')
    return bound_html
