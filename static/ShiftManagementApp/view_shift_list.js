/*ページ(DOM)読み込み後に実行*/
window.onload = function(){

    axios
        .get('/shift-list-ajax/')
        .then((res)=>{
            console.log(res);
            const end_date = new Date(2022,6,30);
            let shift_list_date = document.getElementById('shift_list_date');
            

            let tableEle = document.getElementById('data-table')
            for(let i=1;i<=end_date.getDate();i++){
                let th = document.createElement('th');
                th.innerHTML = '2022/6/'+i;
                shift_list_date.appendChild(th);
            }
            tbody = document.getElementById('tbody')
            tableEle.appendChild(shift_list_date);

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

                console.log(start_date);
                
                //dt = new Date(res.data.shift_lists[i].shift_list[j].date)
                //console.log(dt)
                while(search_date.getDate()<=end_date.getDate()){
                    let td = document.createElement('td'); //毎回定義しないと同じエレメントに上書きされる
                    //console.log(new Date(res.data.shift_lists[i].shift_list[count].date));
                    console.log("search_date:"+search_date);

                    if(count == res.data.shift_lists[i].shift_list.length){
                        td.innerHTML = "test"
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
                        td.innerHTML = "test";

                    }
                    console.log(count);
                    fragment.appendChild(td);
                    search_date.setDate(search_date.getDate()+1);
                }

                
                /*
                if(search_date == res.data.shift_lists[i].shift_list[j]){

                }
                */
                /**
                 * 1日か月末まで回して、shift_listにその日付が存在したら
                 * <td>12:00~18:00</td>
                 * 存在しなければ
                 *<td></td>を代入したい
                    */
                

                tr.appendChild(fragment);
                console.log(tr);
                tbody.appendChild(tr);
  
            }
        })
        .catch((res)=>{
            console.log(res);
        })
    }