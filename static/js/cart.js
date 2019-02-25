//�ȴ��ĵ��������ִ��
$(function(){
    countItem();
    //console.log($('#checkAll').prop('checked'));
    //1.ȫѡ��ȡ��ȫѡ
    var isChecked = false;//��ʶѡ�кͷ�ѡ��״̬
    $("#checkAll").click(function() {

        //ͨ������ѡ��Ԫ��
        isChecked = !isChecked;//ͨ��ȡ����ʾȫѡ
        if (isChecked) {
            $("[name=check]").prop("checked", "true");
        } else {
            $("[name=check]").removeAttr("checked");
        }
        countItem();
    });
        //2.��ѡ
        $("[name=check]").change(function(){
            /*
            ������δ��ѡ�е���Ʒ����==0 ��Ӧȫѡ
            not()��ʾ��ɸѡ
            size()���ڻ�ȡԪ������ ��ͬ��length()
            input:checked����ƥ�䱻ѡ�е�Ԫ��
            */
            if($("[name=check]").not("input:checked").size()==0){
                //�޸�ȫѡ��ť��ѡ��״̬
                $("#checkAll").prop("checked","true");
                //�޸�ȫѡ���
                isChecked = true;
            }else{
                $("#checkAll").removeAttr("checked");
                isChecked = false;
            }
            countItem();
        });
    //3.��������
    $(".add").click(function(){
        //��ȡǰһ���ֵ�Ԫ�ص��ı�����
        var value = $(this).prev().val();
        //�޸��ı����ֵ
        $(this).prev().val(++value);
        //�۸�����������*����
        //ȡpԪ������
        var priceStr = $(this).parent().prev().html();//���ؼ���valȡֵ ��ͨ��html��textȡֵ
        var price = priceStr.substring(1);//��ȡ���۸񣬵��ǽ�ȡ����������ֵ�ַ���"188"
        var sum = price * value;
        //�޸�С��
        //ȡԪ��
        $(this).parent().next().html("<b>&yen;"+sum+"</b>");
        countItem();
    });
    $(".minus").click(function(){
        var value = $(this).next().val();
        if(value>1){
            $(this).next().val(--value);
        }
        //�۸�����������*����
        //ȡpԪ������
        var priceStr = $(this).parent().prev().html();//���ؼ���valȡֵ ��ͨ��html��textȡֵ
        var price = priceStr.substring(1);//��ȡ���۸񣬵��ǽ�ȡ����������ֵ�ַ���"188"
        var sum = price * value;
        //�޸�С��
        //ȡԪ��
        $(this).parent().next().html("<b>&yen;"+sum+"</b>");
        countItem();
    });
    //4.�۸�����(��ʾ�����ʧȥ���㣬Ҳ�����û��Լ������ʱ��)
    //ʧȥ�����¼�����
    $(".count input").blur(function(){
        var value = $(this).val();
        //�����ַ���
        var priceStr = $(this).parent().prev().html();//���ؼ���valȡֵ ��ͨ��html��textȡֵ
        //��ȡ��ֵ
        var price = priceStr.substring(1);//��ȡ���۸񣬵��ǽ�ȡ����������ֵ�ַ���"188"
        var sum = price * value;
        //�޸�С��
        $(this).parent().next().html("<b>&yen;"+sum+"</b>");
        countItem();
    });
    //5.�Ƴ�����
    $(".g-item .action").click(function(){
        //��ȡ��Ԫ��g-item�Ƴ�
        $(this).parent().remove();
    });
    //6.�������۸������ͳ��
    function countItem(){
        var count = 0;//����������
        var price = 0;//�����ܼ۸�
        //��ȡ��ѡ�е���Ʒ����/�۸����ۼ�
        $('[name=check]:checked').each(function(){
            //each()���ڱ�������򼯺ϣ�ÿȡ��һ��Ԫ�أ��Զ�������غ���$(this)ȡ��ѡ���
            count += Number($(this).parents(".g-item").find(".count input").val());
            //��ȡ�۸�
            var priceStr = $(this).parents(".g-item").find(" .sum b").html();//"$188"
            //��ȡ��ת��
            var priceNum  = Number(priceStr.substring(1));
            price += priceNum;
        });
        //�ۼӽ�����ʾ
        //��ʾ�ڹ�����
        $(" .submit-count span").html(count);//��ȡ����
        $(" .submit-price span").html("&yen;"+price);//��ȡ�۸�
    }
});