var authorusername = document.getElementById("authorusername").value;
var accountType = document.getElementById("accountType").value;
//var authorimg = document.getElementById("authorimg").value;
document.write("<!-- Main navbar -->");
document.write("	<div class=\"navbar navbar-inverse\">");
document.write("		<div class=\"navbar-header\">");
document.write("			<a class=\"navbar-brand\" href=\"\/\"><i class=\"icon-atom\"><\/i> IoT Platform<\/a>");
document.write("");
document.write("			<ul class=\"nav navbar-nav pull-right visible-xs-block\">");
document.write("				<li><a data-toggle=\"collapse\" data-target=\"#navbar-mobile\"><i class=\"icon-tree5\"><\/i><\/a><\/li>");
document.write("			<\/ul>");
document.write("		<\/div>");
document.write("");
document.write("		<div class=\"navbar-collapse collapse\" id=\"navbar-mobile\">");
document.write("			<ul class=\"nav navbar-nav\">");
document.write("				<li><a href=\"\/\"><i class=\"icon-home2 position-left\"><\/i> Dashboard<\/a><\/li>");
document.write("");
document.write("				<li><a href=\"\/rawdata\"><i class=\"icon-pulse2 position-left\"><\/i> Raw Data<\/a><\/li>");
document.write("				<li><a href=\"\/analytics/\"><i class=\"icon-stats-growth position-left\"><\/i> Analytics<\/a><\/li>");
document.write("				<li><a href=\"\/reports/\"><i class=\"icon-stack position-left\"><\/i> Reports<\/a><\/li>");
//document.write("                <li><a href=\"\/wallet\"><i class=\"icon-cash4 position-left\"><\/i> Wallet<\/a><\/li>");
//document.write("				<li><a href=\"\/support\"><i class=\"icon-help position-left\"><\/i> Support<\/a><\/li>");
document.write("			<\/ul>");


document.write("			<ul class=\"nav navbar-nav navbar-right\">");



document.write("<li><span class=\"label bg-blue\" style=\"margin-top:14px;\"><i class=\"icon-user position-left\"></i>Admin Account</span><\/li>");

document.write("				<li class=\"dropdown dropdown-user\">");
document.write("					<a class=\"dropdown-toggle\" data-toggle=\"dropdown\">");
//document.write("						<img src=\""+authorimg+"\" alt=\"\">");
document.write("						<span>"+authorusername+"<\/span>");
document.write("						<i class=\"caret\"><\/i>");
document.write("					<\/a>");
document.write("");
document.write("					<ul class=\"dropdown-menu dropdown-menu-right\">");
document.write("						<li><a href=\"\/myprofile\/\"><i class=\"icon-user\"><\/i> My profile<\/a><\/li>");
document.write("						<li class=\"divider\"><\/li>");
document.write("						<li><a href=\"\/account_settings\"><i class=\"icon-cog5\"><\/i> Account settings<\/a><\/li>");
document.write("						<li><a href=\"\/accounts\/logout\"><i class=\"icon-switch2\"><\/i> Logout<\/a><\/li>");
document.write("					<\/ul>");
document.write("				<\/li>");
document.write("			<\/ul>");
document.write("		<\/div>");
document.write("	<\/div>");
document.write("	<!-- \/main navbar -->");
