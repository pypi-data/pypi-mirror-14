<script type="text/javascript">
/**
 * Cajax Communication Core
 * cajax(url) or cajax(url, data)
 * Throws 'ArgumentsNotValidException' in others cases.
 */
var cajax=function(){if(arguments.length>=1 && arguments.length<=2){data=(typeof arguments[1]!=="undefined")?arguments[1]:{};$.ajax({'type':'POST','url':'{% url 'cajax-url' %}?_='+Date.now(),'success':eval,'data':{'url':arguments[0],'data':JSON.stringify(data),'csrfmiddlewaretoken':'{{ csrf_token}}'}});}else{throw 'ArgumentsNotValidException';}}
</script>
