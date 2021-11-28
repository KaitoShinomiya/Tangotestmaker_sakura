let empty_check = () => {
    let start = parseInt(document.getElementById("start").value)
    let end = parseInt(document.getElementById("end").value)
    let how_many = parseInt(document.getElementById("how_many").value)
    let select_or_not = parseInt(document.getElementById("select_or_not").value)
    let sequence_or_random = parseInt(document.getElementById("sequence_or_random").value)
    let which_lang = parseInt(document.getElementById("which_lang").value)
    let which_book = parseInt(document.getElementById("which_book").value)
    console.log(start)
    if (isNaN(start) || isNaN(end) || isNaN(how_many) || select_or_not === -1 || sequence_or_random === -1 || which_lang === -1 || which_book === -1) {
        alert("入力されていない箇所があります。")
        console.log("false")
        return false

    } else {
        if (value_check(start, end, how_many, which_book)) {
            isSmartPhone()
            console.log("true")
            return true
        } else {
            alert("入力した値を確認してください。")
            return false
        }
    }
}

let value_check = (start, end, how_many, which_book) => {
    console.log(which_book)
    console.log(start, end)
    if (end > start) {


        if (which_book === 0) {
            console.log('1')
            return end - (start - 1) >= how_many;
        } else {
            if (which_book === 1) {
                console.log('2')
                if (start > 1900 || end > 1900) {
                    console.log('3')
                    return false
                } else {
                    if (end - (start - 1) < how_many) {
                        console.log('4')
                        return false
                    } else {
                        console.log('5')
                        return true
                    }
                }
            if (which_book === 3) {
                if (start > 735 || end > 735) {
                    console.log('3')
                    return false
                } else {
                    if (end - (start - 1) < how_many) {
                        console.log('4')
                        return false
                    } else {
                        console.log('5')
                        return true
                    }
                }
            }
            } else {
                if (end - (start - 1) < how_many) {
                    console.log('3')
                    return false
                } else {
                    return true
                }
            }

        }
    } else {
        return false
    }
}

let isSmartPhone = () => {
    if (navigator.userAgent.match(/iPhone|Android.+Mobile/)) {
        document.form1.action = '/return_test_sp';
        //スマホ用ウェブアップが完成したらここのリンクを/return_test_spに変更
        return true;
    } else {
        document.form1.action = '/return_test';
        return false;
    }
}



