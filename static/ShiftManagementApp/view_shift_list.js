function view_shift_lists(){

    if($('#selected_month').val()=='none'){
        alert('表示する月を選択してください');
        return 0
    }
    if($('#selected_table').val()=='none'){
        alert('表示するシフトを選択してください');
        return 0
    }
    dispLoading('Loading...');
    const tableEle = document.getElementById('data-table');

    /**表が下に増えていくのを防ぐためクリックするたび表を削除する */
    tableEle.innerHTML = "";

    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
    axios.defaults.xsrfCookieName = "csrftoken"

    let selected_table = '';
    
    if($('#selected_table').val() == 'true'){
        selected_table = true
    }else if($('#selected_table').val() == 'false'){
        selected_table = false
    }

    axios
        .post('/shift-list-ajax/',{
            "selected_month": $('#selected_month').val(),
            "selected_table": selected_table
        })
        .then((res)=>{
            console.log(res);
            let thead_tr = document.createElement('tr');
            const selected_month_str = $('#selected_month').val();
            const selected_month = new Date(Date.parse(selected_month_str));
            console.log(selected_month);
            const dt_last_date = new Date(selected_month.getFullYear(),selected_month.getMonth()+1,0);
            console.log(dt_last_date)

            let th_date_field_header = document.createElement('th');
            th_date_field_header.innerHTML = "#########";
            thead_tr.appendChild(th_date_field_header);
            th_date_field_header.classList.add('fixed01');
            const dayOfWeekStr = [ "日", "月", "火", "水", "木", "金", "土" ]
            
            /**祝日を判定するために祝日APIにGETする */
            axios
                .get('https://holidays-jp.github.io/api/v1/date.json')
                .then((res)=>{
                    const holidays_list = JSON.parse(JSON.stringify(res['data']));
                    console.log(typeof(holidays_list))

                    for(let i=1;i<=dt_last_date.getDate();i++){
                        let th_date= document.createElement('th');
                        dt_year = selected_month.getFullYear();
                        dt_month = selected_month.getMonth()+1;
                        dt_date = selected_month.getDate();
                        dt_day = selected_month.getDay();

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
                        th_date.classList.add('fixed02');
                        selected_month.setDate(selected_month.getDate()+1);
                    }

                })
                .catch((res)=>{
                    alert('エラーが発生しました。再読み込みしてください。')
                })

            const thead = document.createElement('thead');
            thead.appendChild(thead_tr);
            thead.classList.add('sticky-top');

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
                const search_date = new Date(Date.parse(selected_month_str));;

                th.innerHTML = res.data.shift_lists[person_i].username;
                th.classList.add('fixed02');
                tr.appendChild(th);
                
                let count = 0;
                let break_counter = 0;

                /**検索する日付と、その月末が並ぶまでループする*/
                while(search_date.getDate()<=dt_last_date.getDate()){
                    let td = document.createElement('td'); //毎回定義しないと同じエレメントに上書きされる

                    //今月1回もシフトに入っていない場合
                    if(count == res.data.shift_lists[person_i].shift_list.length){
                        td.innerHTML = ""
                    }
                    //検索中の日付とshift_listに格納されている日付が一致した時
                    else if(new Date(res.data.shift_lists[person_i].shift_list[count].date).getTime() == search_date.getTime()){
                        start_date_object = new Date(res.data.shift_lists[person_i].shift_list[count].start);
                        end_date_object = new Date(res.data.shift_lists[person_i].shift_list[count].end);

                        let start_hour_str = start_date_object.getHours();
                        let start_minutes_str = start_date_object.getMinutes();
                        let end_hour_str = end_date_object.getHours();
                        let end_minutes_str = end_date_object.getMinutes();

                        //0埋め
                        start_hour_str = ('0' + start_hour_str).slice(-2);
                        start_minutes_str = ('0' + start_minutes_str).slice(-2);
                        end_hour_str = ('0' + end_hour_str).slice(-2);
                        end_minutes_str = ('0' + end_minutes_str).slice(-2);


                        td.innerHTML = start_hour_str + ":" + start_minutes_str+ "〜" + end_hour_str + ":" + end_minutes_str;

                        //countがshift_listの最後を示しているとき、count+1はundefinedとなるためその場合を避ける
                        if(typeof res.data.shift_lists[person_i].shift_list[count+1] === 'undefined'){

                        }else{
                            while(new Date(res.data.shift_lists[person_i].shift_list[count].date).getTime() == new Date(res.data.shift_lists[person_i].shift_list[count+1].date).getTime()){
                                start_date_object = new Date(res.data.shift_lists[person_i].shift_list[count+1].start);
                                end_date_object = new Date(res.data.shift_lists[person_i].shift_list[count+1].end);
        
                                start_hour_str = start_date_object.getHours();
                                start_minutes_str = start_date_object.getMinutes();
                                end_hour_str = end_date_object.getHours();
                                end_minutes_str = end_date_object.getMinutes();
        
                                //0埋め
                                start_hour_str = ('0' + start_hour_str).slice(-2);
                                start_minutes_str = ('0' + start_minutes_str).slice(-2);
                                end_hour_str = ('0' + end_hour_str).slice(-2);
                                end_minutes_str = ('0' + end_minutes_str).slice(-2);
        
        
                                insert_date = '<br>-------<br>' + start_hour_str + ":" + start_minutes_str+ "〜" + end_hour_str + ":" + end_minutes_str;
                                td.insertAdjacentHTML('beforeend',insert_date)
                                
                                count++;
                                
                                //whileループ中にcountがshift_listの最後を示した場合
                                if(typeof res.data.shift_lists[person_i].shift_list[count+1] === 'undefined'){
                                    break;
                                }
                            }
                        }
                        count++;
                    }
                    //今月1日以上シフトに入っているが、それが検索中の日付ではなかった場合
                    else{
                        td.innerHTML = "";

                    }
                    //console.log(count);
                    fragment.appendChild(td);

                    /**日付が並んでいないか判定
                     * 日付なので、同じ月でsearch_date.getDate()>dt_last_date.getDate()となることはないため
                     * 無限ループになるのを防ぐ*/
                    if(search_date.getDate() == dt_last_date.getDate()){
                        break;
                    }
                    search_date.setDate(search_date.getDate()+1);
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


    