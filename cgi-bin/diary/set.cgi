#! /usr/bin/perl
###############################################################################
# ウェブ日記　環境設定CGI
# Ver 1.0
# http://cgi-garage.parallel.jp/
###############################################################################
use strict;
use CGI;
require "jcode.pl";
my $cgi = CGI::new();
my $chstr;

my $hankaku = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#\$%&'()*+,./:;<=>?\@[\＼]^_`{|}~-";
my $zenkaku = "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ"
       . "０１２３４５６７８９！”＃＄％＆’（）＊＋，．／：；＜＝＞？＠[￥]＾＿‘｛｜｝～－";

my $inpass = $cgi->param('pass');
my %set = &setread("./data/set.cgi");

my $pass = $set{'pass'};
my %COOKIE = ();
my $htcookie = $ENV{'HTTP_COOKIE'};
&getcookie();
my $cookiepass = $COOKIE{'pass'};
my $cryptpass;
if($pass){
	$cryptpass = &auth;
}

my $mainset = $cgi->param('mainset');
my $diary = $cgi->param('diary');
my $gifdel = $cgi->param('gifdel');

##########################
if($mainset){	&mainset;}
if($diary){	&diary;}
if($gifdel){	&gifdel;}
###########################
my $print = "<TABLE border=1>\n<TBODY>\n"
		  . "<TR><TD bgcolor=#cccccc align=center>◆　初期設定</TD>\n"
		  . "<TD><INPUT type=submit name=mainset value=\"初期設定ページへ⇒\"></TD>\n"
		  . "<TD align=center rowspan=2><A href=\"javascript:help('diaryset')\">HELP</A></TD></TR>\n"
		  . "<TR><TD bgcolor=#cccccc align=center>◆　データの入力</TD>\n"
		  . "<TD><INPUT type=submit name=diary value=\"データ入力ページへ⇒\"></TD></TR>\n"
		  . "</TBODY>\n</TABLE>";

my $settemp = &readtemp('./temp/set.html');
if($chstr){
	$settemp =~ s/<!--CHSTR-->/<FONT COLOR=RED>$chstr<\/FONT>/;
}
my $script = "<SCRIPT language='JavaScript'>\n<!--\n";
$script .= "function help(str){\n";
$script .= "\tif(str == 'diaryset'){	window.open('./help/diaryset.html','','width=400,height=200,scrollbars');}\n";
$script .= "}\n//-->\n</SCRIPT>";
$settemp =~ s/<!--SCRIPT-->/$script/;
$settemp =~ s/<!--TITLE-->/ウェブ日記　環境設定CGI/g;
$settemp =~ s/<!--DATA-->/$print/;

my $cookieset = &setcookie("pass",$cryptpass);
print "$cookieset";
print "Content-type:text/html\n\n";
print "$settemp";
exit;

################################################################################
sub gifdel{
	my $gifname = $cgi->param('gifname');
	my $year = $cgi->param('year');
	my $month = $cgi->param('month');

	my $files = "./data/" . $year . sprintf("%02d",$month) . ".cgi";
	my @log = &setread2($files);
	my $newstr;
	for my $i (@log){
		my @i =split (/\t/,$i);
		if($i[1] eq $gifname){
			$newstr .= $i[0] . "\t\t" . $i[2] . "\n";
			unlink($gifname);
		} else{
			$newstr .= $i . "\n";
		}
	}
	$chstr .= &setchange3($newstr,$files);
	&diary();
}

sub diary{
	my $submit = $cgi->param('submit');
	my $del = $cgi->param('del');
	my $before = $cgi->param('beforemonth');
	my $after = $cgi->param('aftermonth');

	my @weekday = ('日','月','火','水','木','金','土');
	my @monthdayArray = (31,28,31,30,31,30,31,31,30,31,30,31);

#####　現在日時　#####
	my @realtime = localtime(time);
	my $realyear = $realtime[5]+1900;
	my $realyear2 = $realtime[5]+1900;
	my $realmonth = $realtime[4]+1;
	my $realmonth2 = $realtime[4]+1;
	my $realday = $realtime[3];
	my $realday2 = $realtime[3];
	my $realweekday = $realtime[6];

	my $cgi = CGI::new();
	my $form_year = $cgi->param('year');
	my $form_month = $cgi->param('month');
	my $form_day = $cgi->param('day');
	my $link = $cgi->param('link');
	if($before){
		$form_month--;
		if($form_month eq 0){
			$form_year--;
			$form_month = 12;
		}
	} elsif($after){
		$form_month++;
		if($form_month eq 13){
			$form_year++;
			$form_month = 1;
		}
	}
	if(($realyear . sprintf("%02d",$realmonth) eq $form_year . sprintf("%02d",$form_month)) && ( $before || $after) ){
		$form_day = "";
	} elsif(($realyear . sprintf("%02d",$realmonth) > $form_year . sprintf("%02d",$form_month)) && $link eq "" && $form_year && $form_month && $del eq ""){
		$form_day = $monthdayArray[$form_month - 1];
	} elsif(($realyear . sprintf("%02d",$realmonth) < $form_year . sprintf("%02d",$form_month)) && $link eq "" && $del eq ""){
		$form_day = 1;
	}

#	print "Content-type:text/html\n\n$form_year $form_month $form_day ";exit;
	if(($form_year ne "")&&($form_month ne "")&&($form_month <= 12)&&($form_day ne "")){
		$realyear = $form_year;
		$realmonth = $form_month;
		$realday = $form_day;
	}
	if((($realyear%4 == 0) && ($realyear%100 != 0)) || ($realyear%400 == 0)){$monthdayArray[1] = 29;}# 閏年の計算

	my $file = "./data/" . $realyear . sprintf("%02d",$realmonth) . ".cgi";
	my @data;
	if(-e $file){
		@data = &setread2($file);
	}

	if($del){
		my $dellog = $form_year . sprintf("%02d",$form_month) . sprintf("%02d",$form_day);
		my $newlog;
		for my $i(@data){
			my @i = split(/\t/,$i);
			if($i[0] ne $dellog){
				$newlog .= $i . "\n";
			} else{
				if(-e $i[1]){
					unlink $i[1];
				}
			}
		}
		$chstr = &setchange3($newlog,$file);
		@data = ();
		push(@data,split(/\t/,$newlog));
	}

	if($submit){
		if(!-e $file){
			open(FP,">>$file");
			close(FP);
		}

		my $gif = $cgi->param('gif');
		my $gif2 = $cgi->param('gif2');
		if($gif eq "" && $gif2){
			my @gif2;
			if($ENV{'HTTP_USER_AGENT'} =~ /Win/ || $ENV{'HTTP_USER_AGENT'} =~ /win/){
				@gif2 = split(/\\/,$gif2);
			} else{
				@gif2 = split(/\//,$gif2);
			}
			$gif = pop(@gif2);
		}
		my $comment = $cgi->param('comment');

		my $newname;
		if($gif){
			my @gif;
			if($ENV{'HTTP_USER_AGENT'} =~ /Win/ || $ENV{'HTTP_USER_AGENT'} =~ /win/){
				@gif = split(/\\/,$gif);
			} else{
				@gif = split(/\//,$gif);
			}
			$newname;
			if($gif2 eq ""){
				$newname .= "./gif/" . $realyear . $realmonth . $realday . "_" . pop(@gif);
			} else{
				$newname .= $gif2;
			}
			if(-e $newname && $gif2 eq ""){
				unlink $newname;
			}
			if($gif2 eq "" && $gif){
				open(OUT, ">$newname") || &errorprint("アップロード失敗","ファイルのアップロードに失敗しました。->$newname");
				binmode (OUT);
				while(<$gif>) {
					print OUT $_;
				}
				close(OUT);
				close ($newname) if ($CGI::OS ne 'UNIX');
			}
		}
		$comment =~ s/\r\n|\r|\n/<!--KAIGYOU-->/g;
		my $hizuke = $realyear . sprintf("%02d",$realmonth) . sprintf("%02d",$realday);
		my $str =  $hizuke. "\t" . $newname . "\t" . $comment . "\n";
		my $newstr;
		my $frag = 0;
		for my $i (@data){
			my @i = split(/\t/,$i);
			if($hizuke eq $i[0]){
				$newstr .= $str;
				if(-e $i[1] && $i[1] ne $newname){
					unlink $i[1];
				}
				$frag++;
			} else{
				$newstr .= $i . "\n";
			}
		}
		if($frag eq 0){
			$newstr .= $str;
		}
		$chstr = &setchange3($newstr,$file);
		@data = ();
		@data = split(/\n/,$newstr);
	}

#####　今月1日の曜日　#####
	my $m = $realmonth;
	my $y = $realyear;
	if ($m < 3) { --$y; $m += 12; }# ツェラー公式
	my $weekday = int(($y+int($y/4) - int($y/100) + int($y/400) + int((13*$m+8)/5) + 1) % 7);


#####　今月の日数　######
	my $endday = $monthdayArray[$realmonth-1];

	my $cellprint = "<input type=submit name=\"beforemonth\" value=\"←前の月\"> 　 \n"
				  . "<input type=submit name=\"aftermonth\" value=\"次の月→\">\n"
				  . "<TABLE border=1>\n<TBODY>\n"
				  . "<TR><TD align='center' colspan=7><FONT size=-1>$realyear年$realmonth月</FONT></TD></TR>\n<TR>";
	my $count = 0;
	for my $i(@weekday){
		$cellprint .= "<TD align=center>";
		if($count eq 0){
			$cellprint .= "<FONT COLOR=RED SIZE=\"-1\">";
		} elsif($count eq 6){
			$cellprint .= "<FONT COLOR=BLUE SIZE=\"-1\">";
		} else{
			$cellprint .= "<FONT SIZE=\"-1\">";
		}
		$cellprint .= "$i</FONT></TD>\n";
		$count++;
	}
	$cellprint .= "</TR>\n";
	for(my $i = 0;$i < $weekday;$i++){# 月初日までの空白
		if($i eq 0){
			$cellprint .= "<TR>";
		}
		$cellprint .= "<TD></TD>";
	}
	for(my $i = 1; $i <= $endday; $i++){# 日にち入力
		if($weekday eq 0){
			$cellprint .= "<TR>"
		}
		if($i eq $realday){
			$cellprint .= "<TD bgcolor='pink' align='center'>";
		} else{
			$cellprint .= "<TD align='center'>";
		}
		if($weekday eq 0){
			$cellprint .= "<FONT COLOR='red' SIZE=\"-1\">";
		} elsif($weekday eq 6){
			$cellprint .= "<FONT COLOR='BLUE' SIZE=\"-1\">";
		} else{
			$cellprint .= "<FONT SIZE=\"-1\">";
		}
		$cellprint .= "<A href=set.cgi?diary=aaa&year=$realyear&month=$realmonth&day=$i&link=aaa>$i</A></FONT></TD>\n";
		if($weekday eq 6){
			$cellprint .= "</TR>\n";
			$weekday = 0;
		} else{
			$weekday++;
		}
	}
	if($weekday ne 0){# 日付終了後のセル
		for(my $i = $weekday; $i < 7; $i++){
			$cellprint .= "<TD></TD>\n";
		}
		$cellprint .= "</TR>\n";
	}

	my @todaydata;
	my $today = $realyear . sprintf("%02d",$realmonth) . sprintf("%02d",$realday);
	for my $i(@data){
		my @i = split(/\t/,$i);
		if($i[0] eq $today){
			push(@todaydata,@i);
			next;
		}
	}
	$todaydata[2] =~ s/<!--KAIGYOU-->/\n/g;
	my $files;
	if($todaydata[1]){
		$files = "<A href=\"$todaydata[1]\">$todaydata[1]</A>";
	} else{
		$files = "無し";
	}
	$cellprint .= "</TBODY></TABLE>\n"
				. "<BR>\n<HR>\n"
				. "<B>◆ 　 $realyear\年$realmonth\月$realday\日</B>\n<BR>\n<BR>\n"
				. "◆　現在の画像ファイル　 $files ";
	if($todaydata[1]){
		$cellprint .= "　 <A href=\"set.cgi?gifdel=aaa&gifname=$todaydata[1]&year=$realyear&month=$realmonth&day=$realday&link=aaa\">この画像を削除する</A>";
	}
	if($todaydata[1]){
		$cellprint .= "<input type=hidden name=gif2 value=\"$todaydata[1]\">\n";
	}
	$cellprint .= "<BR>\n<BR>\n"
				. "◆　画像ファイルアップロード　<input type=\"file\" name=\"gif\" size=\"60\">\n<BR>\n<BR>\n"
				. "◆　日記<BR>\n"
				. "<TEXTAREA rows=\"10\" cols=\"80\" name=\"comment\">$todaydata[2]</TEXTAREA><BR>\n<BR>\n"
				. "<INPUT type=\"submit\" name=\"submit\" value=\"日記を登録\">\n";
	if($todaydata[0]){
		$cellprint .= " 　 <INPUT type=\"submit\" name=\"del\" value=\"この日のデータを削除する\">\n";
	}
	$cellprint .= "<INPUT type=\"hidden\" name=\"diary\" value=\"aaa\">\n"
				. "<INPUT type=\"hidden\" name=\"year\" value=\"$realyear\">\n"
				. "<INPUT type=\"hidden\" name=\"month\" value=\"$realmonth\">\n"
				. "<INPUT type=\"hidden\" name=\"day\" value=\"$realday\">\n";

	my $settemp = &readtemp('./temp/set.html');
	if($chstr){
		$settemp =~ s/<!--CHSTR-->/<FONT COLOR=RED>$chstr<\/FONT>/;
	}
	my $script = "<SCRIPT language='JavaScript'>\n<!--\n";
	$script .= "function help(str){\n";
	$script .= "\tif(str == 'itiran'){	window.open('./help/itiran.html','','width=400,height=150,scrollbars');}\n";
	$script .= "}\n//-->\n</SCRIPT>";

	$settemp =~ s/<!--SCRIPT-->/$script/;
	$settemp =~ s/<!--TITLE-->/ウェブ日記　データ入力/g;
	$settemp =~ s/<!--DATA-->/$cellprint/;

	print "Content-type:text/html\n\n";
	print "$settemp";
	exit;
}

sub upfilename{
	my $filename = shift;
	$filename =~ tr/A-Z/a-z/;
	$filename =~ s/(?:%20)+/_/g;
	$filename =~ s/%[\da-fA-F]{2}//g;
	return $filename;
}

sub mainset{
	my $settemp = &readtemp('./temp/set.html');
	my $henkou = $cgi->param('henkou');

	if($henkou){
		my $password = $cgi->param('password');
		my $newpass = $cgi->param('newpass');
		my $topadd = $cgi->param('topadd');
		my $title = $cgi->param('title');
		my $wall = $cgi->param('wall');
		my $gifwidth = $cgi->param('gifwidth');
		my $gifheight = $cgi->param('gifheight');
		my $headhtml = $cgi->param('headhtml');
		$headhtml =~ s/\r\n|\r|\n/<!--KAIGYOU-->/g;
		my @setkey = ('pass','topadd','title','wall','gifwidth','gifheight','headhtml');
		jcode::tr(\$gifwidth, $zenkaku, $hankaku);
		jcode::tr(\$gifheight, $zenkaku, $hankaku);

		my $newpassword;
		if($password || $newpass){
			$newpassword = &passchange($password,$newpass);
		} unless($newpassword){
			$newpassword = $set{'pass'};
		} if($gifheight =~ /[^0-9]/ || $gifwidth =~ /[^0-9]/){
			&errorprint("入力エラー","画像の幅と高さは半角数値で入力してください");
		}

		my @setvalue = ($newpassword,$topadd,$title,$wall,$gifwidth,$gifheight,$headhtml);
		$chstr = &setchange('./data/set.cgi',\@setkey,\@setvalue);
		%set = &setread("./data/set.cgi");
	}

	$set{'headhtml'} =~ s/<!--KAIGYOU-->/\n/g;
	my $print = "<TABLE border=1>\n<TBODY>\n"
			  . "<TR><TD bgcolor=#cccccc>パスワード変更</TD>\n"
			  . "<TD>現在のパスワード　<INPUT size=20 type=password name=password><BR>"
			  . "変更するパスワード<INPUT size=20 type=password name=newpass></TD>\n"
			  . "<TD rowspan=6><A href=\"javascript:help('mainset')\">HELP</A></TD></TR>\n"
			  . "<TR><TD bgcolor=#cccccc>トップページアドレス</TD>\n"
			  . "<TD><INPUT size=60 type=text name=topadd value='$set{'topadd'}'></TD></TR>\n"
			  . "<TR><TD bgcolor=#cccccc>日記タイトル</TD>\n"
			  . "<TD><INPUT size=40 type=text name=title value='$set{'title'}'></TD></TR>\n"
			  . "<TR><TD bgcolor=#cccccc>壁紙</TD>\n"
			  . "<TD><INPUT size=40 type=text name=wall value='$set{'wall'}'></TD></TR>\n"
			  . "<TR><TD bgcolor=#cccccc>画像サイズ</TD>\n"
			  . "<TD>幅<INPUT size=5 type=text name=gifwidth value='$set{'gifwidth'}'>"
			  . "　高さ<INPUT size=5 type=text name=gifheight value='$set{'gifheight'}'></TD></TR>\n"
			  . "<TR><TD bgcolor=#cccccc>ヘッダーHTML</TD>\n"
			  . "<TD><TEXTAREA name=\"headhtml\" rows=\"10\" cols=\"80\">$set{'headhtml'}</TEXTAREA></TD></TR>\n"
			  . "<TR><TD colspan=3 align=center><INPUT type=submit name=henkou value='設定を変更する'></TD></TR>\n"
			  . "</TBODY><INPUT type=hidden name=mainset value=aaa></TABLE>\n";

	if($chstr){
		$settemp =~ s/<!--CHSTR-->/<FONT COLOR=RED>$chstr<\/FONT>/;
	}
	my $script = "<SCRIPT language='JavaScript'>\n<!--\n";
	$script .= "function help(str){\n";
	$script .= "\tif(str == 'mainset'){	window.open('./help/mainset.html','','width=400,height=300,scrollbars');}\n";
	$script .= "}\n//-->\n</SCRIPT>";
	$settemp =~ s/<!--SCRIPT-->/$script/;
	$settemp =~ s/<!--TITLE-->/ウェブ日記　環境設定CGI/g;
	$settemp =~ s/<!--DATA-->/$print/;
	my $cookieset = &setcookie("pass",$set{'pass'});

	print "Content-type:text/html\n\n";
	print "$settemp";
	exit;
}

sub passchange{
	my ($oldpass,$np) = @_;
	my $cnp = crypt($np,'ps');
	my $coldpass = crypt($oldpass,'ps');
	if($set{'pass'} ne $coldpass && $set{'pass'}){
		print "content-type:text/html\n\nパスワードが違います。入力しなおしてください。";	exit;
	} else{
		my $cookieset = &setcookie("pass",$cnp);
		print "$cookieset";
	}
	return $cnp;
}

sub setchange(){
	my($setfile,$key,$value) = @_;
	my @key = @{$key};
	my @value = @{$value};
	my $data;
	my $count = 0;
	foreach my $i(@key){
		$data .= $i . "=" . $value[$count] . "\n";
		$set{$i} = $value[$count];
		$count++;
	}

	open(SET,"+<$setfile")||die &errorprint("Datafile Open Error!","設定ファイルが開けません。->$setfile");
	&file_lock(*SET);
	seek(SET,0,0);
	truncate(SET,0);
	print SET $data;
	close(SET);

	my $changestr = "設定を変更しました。";
	return $changestr;
}

sub setchange2(){
	my($changestr,$changefile) = @_;

	open(SET,">>$changefile")||die &errorprint("Datafile Open Error!","設定ファイルが開けません。->$changefile");
	&file_lock(*SET);
	print SET $changestr;
	close(SET);

	my $changestr = "設定を変更しました。";
	return $changestr;
}

sub setchange3(){
	my($changelist,$changefile) = @_;

	open(SET,">>$changefile")||die &errorprint("Datafile Open Error!","設定ファイルが開けません。->$changefile");
	&file_lock(*SET);
	seek(SET,0,0);
	truncate(SET,0);
	print SET $changelist;
	close(SET);

	my $changestr = "設定を変更しました。";
	return $changestr;
}

sub readtemp{
	my($template) = @_;
	open(DAT,"<$template")||die &errorprint("templateData Open Error!","テンプレートファイルが開けません。->$template");

	&file_lock(*DAT);
	my $data;
	while(my $line = <DAT>){
		$data .= $line;
	}
	close(DAT);
	return $data;
}

sub file_lock{
	local(*LOGS) = @_;
	eval{flock(LOGS,2);};
	if($@){
		&errorprint("flock Error!","ファイルロックが使えません。");
	}
}

sub setread(){
	my ($setdat) = @_;
	my %data = ();
	open(LOGS,"<$setdat")||die &errorprint("file open error!","設定ファイルが開けません。ファイルが存在するか、ファイルのパーミッションを確認してください。->$setdat");
	&file_lock(*LOGS);
	while(<LOGS>){
		chomp;
		if(/^([a-zA-Z0-9\_\-]+)\=(.+)$/) {
			my $key = $1;
			my $value = $2;
			unless($key) {next;}
			$key =~ s/^[\s\t]*//;
			$key =~ s/[\s\t]*$//;
			$value =~ s/^[\s\t]*//;
			$value =~ s/[\s\t]*$//;
			$data{$key} = $value;
		}
	}
	close(LOGS);
	return %data;
}

sub setread2(){
	my ($setdat) = @_;
	my @data;

	open(LOGS,"<$setdat")||die &errorprint("file open error!","設定ファイルが開けません。ファイルが存在するか、ファイルのパーミッションを確認してください。->$setdat");
	&file_lock(*LOGS);
	while(my $line = <LOGS>){
		chomp($line);
		push(@data,$line);
	}
	close(LOGS);
	return @data;
}

sub auth(){
	my $error;
	my $ercount;
	my $cpass;
	$cpass = crypt($inpass,'ps');
	if($cpass ne $pass && $cookiepass ne $pass){
		$ercount = 1;
		if($inpass ne ""){
			$error = "<FONT color='red'>パスワードが一致しません！</FONT>";
		}
	} if($ercount){
		my $temp = &readtemp("temp/admin.html");
		$temp =~ s/<!--ERROR-->/$error/;
		print "Content-type:text/html\n\n";
		print "$temp";
		exit;
		1;
	} if($cookiepass eq $pass){
		$cpass = $cookiepass;
	}
	return $cpass;
}

###クッキーのゲット
sub getcookie {
	my ($tmp, $name, $value);
	for $tmp (split(/; */, $ENV{'HTTP_COOKIE'})) {
		($name, $value) = split(/=/, $tmp);
		$value =~ s/\%([0-9a-fA-F][0-9a-fA-F])/pack("C", hex($1))/eg;
		$COOKIE{$name} = $value;
	}
}

###クッキーのセット ########################################################
sub setcookie {
	my ($tmp, $val);
	$val = $_[1];
	$val =~ s/(\W)/sprintf("%%%02X", unpack("C", $1))/eg;
	$tmp = "Set-Cookie:";
	$tmp .= "$_[0]=$val;\n";
	return($tmp);
}

sub hostname {
	my($ip_address) = @_;
	my(@addr) = split(/\./, $ip_address);
	my($packed_addr) = pack("C4", $addr[0], $addr[1], $addr[2], $addr[3]);
	my($name, $aliases, $addrtype, $length, @addrs);
	($name, $aliases, $addrtype, $length, @addrs) = gethostbyaddr($packed_addr, 2);
	unless($name){
		$name = $ip_address;
	}
	return $name;
}

sub errorprint{
	my ($title,$erstr) = @_;
	print "content-type:text/html\n\n";
	print "<HTML>\n<HEAD>\n";
	print "<LINK rel=stylesheet href=cgigarage.css type=text/css>\n";
	print "<TITLE>$title</TITLE>\n</HEAD>\n";
	print "<BODY>\n<H1>$title</H1>\n";
	print "<P>$erstr<BR></P>\n<HR>\n";
	print "<A href=http://cgi-garage.parallel.jp/>CGI-Garage</A>\n";
	print "</BODY>\n</HTML>\n";
	exit;
}