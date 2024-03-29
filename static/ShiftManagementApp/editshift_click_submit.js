/**editshift_click_newshift.jsで使うためにshow_timeline()をグローバル変数に代入する*/
$(document).on('click','#submit-date',window.show_timeline =  function show_timeline() {
            
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
    axios.defaults.xsrfCookieName = "csrftoken"
    
    $('#submit-date').off('click') //offでクリックイベントを削除することで複数登録を防ぐ
        dispLoading('Loading...');
        
        //「新規シフト作成」ボタンを押した時に予めフォームに日付を入れるために、グローバル変数に代入 
        //editshift_click_newshift.jsで使用
        window.date_of_sending = $('#edit-date').val();

        axios
            .post("/edit-shift-Ajax/",{
                    "date":$('#edit-date').val()
            })
            .then((res)=>{
                
                if(res.data.length == 0){
                    const no_shift_alert = document.getElementById('no_shift_alert');
                    no_shift_alert.innerHTML = '<b>シフトが存在しないか、公開されていません</b>'
                   //$('#no_shift_alert').modal('show');
                }
                
                google.charts.load('current', {'packages':['timeline']});
                google.charts.setOnLoadCallback(drawChart);
                function drawChart() {
                    var container = document.getElementById('timeline');
                    var chart = new google.visualization.Timeline(container);
                    var dataTable = new google.visualization.DataTable();

                    dataTable.addColumn({ type: 'string', id: 'name' });
                    dataTable.addColumn({ type: 'string', id: 'shift_id' });
                    dataTable.addColumn({ type: 'string', id: 'style' ,role: 'style' });
                    dataTable.addColumn({ type: 'date', id: 'start' });
                    dataTable.addColumn({ type: 'date', id: 'end' });
                    /*barlabelの場所（カラム２）は何も入れなくても存在してないとうまく動かない*/
                    console.log(res.data)
                    for (let i=0;i<res.data.length;i++){
                        let name = res.data[i]['name'];
                        let shift_id = String(res.data[i]['shift_id']);
                        let style = res.data[i]['style'];
                        let start = res.data[i]['start'];
                        let end = res.data[i]['end'];
                        dataTable.addRows([
                            [name,shift_id,style,new Date(start),new Date(end)]
                        ]);
                    }
                    let option = {
                        timeline:{
                            showBarLabels:false//バーラベルをOFF、shift_idが入ってる
                        },
                        tooltip:{//ツールチップ（マウスオーバーで出てくるやつをOFF）
                            trigger:'none'
                        },
                    }

                    chart.draw(dataTable,option);
                    removeLoading();
                    console.log(dataTable);
                    //クリックイベントを拾う
                    google.visualization.events.addListener(chart, 'select', function (e) {
                        
                        var selection = chart.getSelection();
                        let row = selection['0']['row']
                        console.log(row);//選択したバーのdataTableにおけるrow
                        console.log(dataTable['Wf'][row]['c']['1']['v']);//shift_idを表示

                        const shift_id_modal = dataTable['Wf'][row]['c']['1']['v'];
                        const date_modal = moment(dataTable['Wf'][row]['c']['3']['v']).format('YYYY-MM-DD');
                        const start_modal = moment(dataTable['Wf'][row]['c']['3']['v']).format('HH:mm');
                        const end_modal = moment(dataTable['Wf'][row]['c']['4']['v']).format('HH:mm');
                        console.log(typeof(dataTable['Wf'][row]['c']['2']['v'])); 
                        let position;
                        if (dataTable['Wf'][row]['c']['2']['v'] == '#0000ff'){//blue
                            position = 'True';
                        }else if(dataTable['Wf'][row]['c']['2']['v'] == '#ff0000'){//red
                            position = 'False';
                        }else{
                            console.log('不正な値')
                        }
                        console.log(position);
                        $('#shift_id').val(shift_id_modal)
                        $('#date').val(date_modal);
                        $('#position').val(position);
                        $('#start').val(start_modal);
                        $('#end').val(end_modal);
                        $('#testModal').modal('show');
                        $('#submit-shift').off('click') //offでクリックイベントを削除することで複数登録を防ぐ
                        /*モーダル内の送信ボタンを押したときの動作*/
                        $('#submit-shift').click(function(){
                            dispLoading('Loading...');
                            
                            const start = new Date(`${$('#edit-date').val()}T${$('#start').val()}:00.000+09:00`);
                            const end = new Date(`${$('#edit-date').val()}T${$('#end').val()}:00.000+09:00`);

                            // バリデーション
                            if (start > end){
                                removeLoading();
                                alert("終了時刻は開始時刻より後である必要があります");
                                return;
                            }
                            axios
                                .post("/edit-shift-Ajax/post-shiftdata/",{
                                    "id":Number($('#shift_id').val()),//int型に変換
                                    "member":null,
                                    "position":($('#position').val()),
                                    "date":$('#edit-date').val(),
                                    "start":$('#edit-date').val()+"T"+$('#start').val(),
                                    "end":$('#edit-date').val()+"T"+$('#end').val()
                                })
                                .then((res)=>{
                                    if(res.data.res_code){
                                        $('#testModal').modal('hide');//modalを閉じる
                                        show_timeline();//シフト表再描画させる
                                    }else{
                                        alert('データベースの更新に失敗しました');
                                    }
                                })
                                .catch((error)=>{
                                    alert('送信失敗しました');
                                    console.log(error);
                                })
                                .finally(()=>{
                                    removeLoading();
                                })

                        });
                        /*モーダル内の削除ボタンを押したときの動作*/
                        $('#delete-shift').click(function(){
                            axios
                                .post("/edit-shift-Ajax/post-shiftdata/delete-shiftdata/",{
                                    "id":Number($('#shift_id').val()),//int型に変換
                                })
                                .then((res)=>{
                                    //alert('送信成功');
                                    $('#testModal').modal('hide');//modalを閉じる
                                    show_timeline();//シフト表再描画させる
                                })
                                .catch(()=>{
                                    alert('送信失敗しました');
                                })
                        })
                    });
                }
            })
            .catch(()=>{
                alert("送信失敗しました");
            })
            .finally(()=>{
                removeLoading();
            })

});