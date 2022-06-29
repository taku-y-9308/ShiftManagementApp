/*ページ(DOM)読み込み後に実行*/
window.onload = function(){

    axios
        .get('/shift-list-ajax/')
        .then((res)=>{
            console.log(res);
            const end_date = new Date(2022,6,31);
            let shift_list_date = document.getElementById('shift_list_date');
            const dt = new Date(2022,6,1)
            const dt_last_date = new Date(dt.getFullYear(),dt.getMonth()+1,0);
            //console.log(dt_last_date)
            for(let i=1;i<=dt_last_date.getDate();i++){
                let th = document.createElement('th');
                dt_month = dt.getMonth();
                dt_date = dt.getDate();
                th.innerHTML = dt_month + "/" + dt_date;
                shift_list_date.appendChild(th);
                dt.setDate(dt.getDate()+1);
            }
            //console.log(end_date.getDate());
            //tableEle.appendChild(shift_list_date);
            tbody = document.getElementById('tbody')

            /**個人ごとにループを回す */
            for(let i=0;i<res.data.shift_lists.length;i++){
                let tr = document.createElement('tr');
                let th = document.createElement('th');
                let td = document.createElement('td');
                let fragment = document.createDocumentFragment();
                const start_date = new Date(2022,6,1,9,0,0);
                const search_date = start_date;

                th.innerHTML = res.data.shift_lists[i].username;
                tr.appendChild(th)

                let count = 0;
                let break_counter = 0;

                //console.log(start_date);
                //dt = new Date(res.data.shift_lists[i].shift_list[j].date)
                //console.log(dt)
                while(search_date.getDate()<=dt_last_date.getDate()){
                    let td = document.createElement('td'); //毎回定義しないと同じエレメントに上書きされる
                    //console.log(new Date(res.data.shift_lists[i].shift_list[count].date));
                    //console.log("search_date:"+search_date);
                    console.log(search_date.getDate());
                    console.log(end_date.getDate());

                    if(count == res.data.shift_lists[i].shift_list.length){
                        td.innerHTML = ""
                    }
                    else if(new Date(res.data.shift_lists[i].shift_list[count].date).getTime() == search_date.getTime()){
                        start_date_object = new Date(res.data.shift_lists[i].shift_list[count].start);
                        end_date_object = new Date(res.data.shift_lists[i].shift_list[count].end);

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
  
            }
        })
        .catch((res)=>{
            console.log(res);
        })
    }