function print_shift_lists(is_first_half_second_half){

    if($('#selected_month').val()=='none'){
        alert('月を選択してください')
    }
    dispLoading('Loading...');
    const tableEle = document.getElementById('data-table');

    /**表が下に増えていくのを防ぐためクリックするたび表を削除する */
    tableEle.innerHTML = "";

    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
    axios.defaults.xsrfCookieName = "csrftoken"

    axios
        .post('/shift-list-ajax/',{
            "selected_month": $('#selected_month').val()
        })
        .then((res)=>{
            console.log(res);
            let thead_tr = document.createElement('tr');
            const selected_month_str = $('#selected_month').val();
            const selected_month = new Date(Date.parse(selected_month_str));
            console.log(selected_month);

            let th_date_field_header = document.createElement('th');
            th_date_field_header.innerHTML = "#";
            thead_tr.appendChild(th_date_field_header);
            const dayOfWeekStr = [ "日", "月", "火", "水", "木", "金", "土" ]
            
            /**祝日を判定するために非同期で祝日APIにGETする */
            axios
                .get('https://holidays-jp.github.io/api/v1/date.json')
                .then((res)=>{
                    const holidays_list = JSON.parse(JSON.stringify(res['data']));
                    console.log(typeof(holidays_list))

                    //前半表示か後半表示でで表示する日付の範囲を変える
                    if(is_first_half_second_half){
                        var dt_start_date_for_display = new Date(selected_month.getFullYear(),selected_month.getMonth(),1,9,0,0);
                        var dt_last_date_for_display = new Date(selected_month.getFullYear(),selected_month.getMonth(),15,9,0,0);
                    }
                    else{
                        var dt_start_date_for_display = new Date(selected_month.getFullYear(),selected_month.getMonth(),16,9,0,0);
                        var dt_last_date_for_display = new Date(selected_month.getFullYear(),selected_month.getMonth()+1,0,9,0,0);
                    }

                    //start_dateとlast_dateの間の分だけループする
                    const difference_of_start_and_end = dt_last_date_for_display.getDate()-dt_start_date_for_display.getDate()+1;
                    for(let i=1;i<=difference_of_start_and_end;i++){
                        let th_date= document.createElement('th');
                        dt_year = dt_start_date_for_display.getFullYear();
                        dt_month = dt_start_date_for_display.getMonth()+1;
                        dt_date = dt_start_date_for_display.getDate();
                        dt_day = dt_start_date_for_display.getDay();

                        const date_for_holiday_check = dt_year + "-"+ ('0'+dt_month).slice(-2) + "-" + ('0'+dt_date).slice(-2);
                        th_date.innerHTML = dt_month + "/" + dt_date + "<br>"
                        /**祝日判定 */
                        //祝日の場合
                        if(date_for_holiday_check in holidays_list){
                            th_date.insertAdjacentHTML('beforeend',"<span style='color:red'>" +dayOfWeekStr[dt_day] + "</span>");
                        }
                        //土曜日の場合
                        else if(dt_day==6){
                            th_date.insertAdjacentHTML('beforeend',"<span style='color:blue'>" +dayOfWeekStr[dt_day] + "</span>");
                        }
                        //日曜日の場合
                        else if(dt_day==0){
                            th_date.insertAdjacentHTML('beforeend',"<span style='color:red'>" +dayOfWeekStr[dt_day] + "</span>");
                        }
                        //平日の場合
                        else{
                            th_date.innerHTML = dt_month + "/" + dt_date + "<br>" +dayOfWeekStr[dt_day];
                        }
                        thead_tr.appendChild(th_date);
                        dt_start_date_for_display.setDate(dt_start_date_for_display.getDate()+1);
                    }

                })
                .catch((res)=>{
                    alert('エラーが発生しました。再読み込みしてください。')
                })

            const thead = document.createElement('thead');
            thead.appendChild(thead_tr);

            tableEle.appendChild(thead);
            //console.log(end_date.getDate());
            //tableEle.appendChild(shift_list_date);
            tbody = document.createElement('tbody')

            /**個人ごとにループを回す */
            for(let person_i=0;person_i<res.data.shift_lists.length;person_i++){
                let tr = document.createElement('tr');
                let th = document.createElement('th');
                let td = document.createElement('td');
                let fragment = document.createDocumentFragment();

                const dt_start_date = new Date(selected_month.getFullYear(),selected_month.getMonth(),1,9,0,0);
                const dt_last_date = new Date(selected_month.getFullYear(),selected_month.getMonth()+1,0,9,0,0);

                const search_date = new Date(Date.parse(selected_month_str));;

                th.innerHTML = res.data.shift_lists[person_i].username;
                tr.appendChild(th)

                let count = 0;
                let break_counter = 0;

                /**検索する日付と、その月末が並ぶまでループする*/
                while(dt_start_date.getDate()<=dt_last_date.getDate()){

                    let td = document.createElement('td'); //毎回定義しないと同じエレメントに上書きされる

                    if(count == res.data.shift_lists[person_i].shift_list.length){
                        td.innerHTML = ""
                    }
                    else if(new Date(res.data.shift_lists[person_i].shift_list[count].date).getTime() == dt_start_date.getTime()){
                        start_date_object = new Date(res.data.shift_lists[person_i].shift_list[count].start);
                        end_date_object = new Date(res.data.shift_lists[person_i].shift_list[count].end);

                        start_hour_str = start_date_object.getHours();
                        start_minutes_str = start_date_object.getMinutes();
                        end_hour_str = end_date_object.getHours();
                        end_minutes_str = end_date_object.getMinutes();

                        //0埋め
                        start_hour_str = ('0' + start_hour_str).slice(-2);
                        start_minutes_str = ('0' + start_minutes_str).slice(-2);
                        end_hour_str = ('0' + end_hour_str).slice(-2);
                        end_minutes_str = ('0' + end_minutes_str).slice(-2);


                        td.innerHTML = start_hour_str + ":" + start_minutes_str+ "〜" + end_hour_str + ":" + end_minutes_str;
                        count++;
                    }
                    else{
                        td.innerHTML = "";

                    }

                    /**日付が並んでいないか判定
                     * 日付なので、同じ月でsearch_date.getDate()>dt_last_date.getDate()となることはないため
                     * breakして無限ループになるのを防ぐ*/
                    if(dt_start_date.getDate() == dt_last_date.getDate()){
                        fragment.appendChild(td);
                        break;
                    }

                    //前半表示：検索中の日付が15日以下ならHTMLに追加する
                    //後半表示：検索中の日付が16日以上ならHTMLに追加する
                    if(is_first_half_second_half){
                        if(dt_start_date.getDate()<=15){
                            fragment.appendChild(td);
                        }
                    }
                    else{
                        if(dt_start_date.getDate()>=16){
                            fragment.appendChild(td);
                        }
                    }
                    
                    dt_start_date.setDate(dt_start_date.getDate()+1);
                }
                tr.appendChild(fragment);
                console.log(tr);
                tbody.appendChild(tr);
                tableEle.appendChild(tbody);
            }
        })
        .catch((res)=>{
            console.log(res);
        })
        .finally(()=>{
            removeLoading();
        })
    }


    