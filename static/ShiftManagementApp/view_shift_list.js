/*ページ(DOM)読み込み後に実行*/
//window.onload = 
function view_shift_lists(){
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
            const selected_month = $()
            const date_for_display = new Date(2022,6,1)
            const dt_last_date = new Date(date_for_display.getFullYear(),date_for_display.getMonth()+1,0);
            console.log(dt_last_date)
            for(let i=1;i<=dt_last_date.getDate();i++){
                let th = document.createElement('th');
                dt_month = date_for_display.getMonth()+1;
                dt_date = date_for_display.getDate();
                th.innerHTML = dt_month + "/" + dt_date;
                thead_tr.appendChild(th);
                date_for_display.setDate(date_for_display.getDate()+1);
            }

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
                const start_date = new Date(2022,6,1,9,0,0);
                const search_date = start_date;

                th.innerHTML = res.data.shift_lists[person_i].username;
                tr.appendChild(th)

                let count = 0;
                let break_counter = 0;

                //console.log(start_date);
                //dt = new Date(res.data.shift_lists[person_i].shift_list[j].date)
                //console.log(dt)

                /**検索する日付と、その月末が並ぶまでループする*/
                while(search_date.getDate()<=dt_last_date.getDate()){
                    let td = document.createElement('td'); //毎回定義しないと同じエレメントに上書きされる

                    if(count == res.data.shift_lists[person_i].shift_list.length){
                        td.innerHTML = ""
                    }
                    else if(new Date(res.data.shift_lists[person_i].shift_list[count].date).getTime() == search_date.getTime()){
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
                     * 無限ループになるのを防ぐ*/
                    if(search_date.getDate() == dt_last_date.getDate()){
                        fragment.appendChild(td);
                        break;
                    }

                    //console.log(count);
                    fragment.appendChild(td);
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
    }


    