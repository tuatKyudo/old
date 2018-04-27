#! /usr/bin/perl 
###############################################################################
# ウェブ日記
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

my %set = &setread("./data/set.cgi");
$set{'headhtml'} =~ s/<!--KAIGYOU-->/\n/g;

print "content-type:text/html\n\n"
	. "<HTML>\n"
	. "<HEAD>\n"
	. "<META http-equiv=\"Content-Type\" content=\"text/html; charset=Shift_JIS\">\n"
	. "<META http-equiv=\"Content-Style-Type\" content=\"text/css\">\n"
	. "<LINK rel=\"STYLESHEET\" type=\"TEXT/CSS\" href=\"cgigarage.css\">\n"
	. "<TITLE>$set{'title'}</TITLE>\n"
	. "</HEAD>\n"
	. "<BODY  background=\"$set{'wall'}\">\n";
if($set{'topadd'}){
	print "<P>[ <A href=\"$set{'topadd'}\">トップページ</A> ]<br>"
		."<IMG src=\"../fstat/fcount.cgi?LOG=hitorigoto&DIGIT=4&FONT=fuksan\" width=\"20\" height=\"8\" border=\"0\"></P>";
}
print "<CENTER>\n"
	."<TABLE border=\"0\" width=\"750\">\n<TBODY>\n"
	. "<TR>\n"
	. "<TD colspan=\"2\" width=\"750\">\n"
	. "$set{'headhtml'}</TD>\n"
	. "</TR>\n"
	. "<TR>\n"
	. "<TD width=\"200\" align=center>\n";
my ($daydat,$print) = &calendarprint();
print "$print</TD>\n"
	. "<TD background=\"wallppr004.gif\" width=\"550\" align=center bgcolor=\"#ffffff\">\n";
if($daydat){
	my @daydat = split(/\t/,$daydat);
	my $hizuke = substr($daydat[0],0,4) . "/" . substr($daydat[0],4,2) . "/" . substr($daydat[0],6,2);
	$daydat[2] =~ s/<!--KAIGYOU-->/<BR>/g;
	print "<BR>\n"
		. "<TABLE border=\"0\" width=\"99%\">\n"
		. "<TBODY>\n"
		. "<TR>\n"
		. "<TD width=\"70\"></TD>\n"
		. "<TD align=\"center\">\n"
		. "<H2>$hizuke</H2>\n";
	if($daydat[1]){
		print "<IMG src=\"$daydat[1]\"";
		if($set{'gifwidth'}){
			print " width=\"$set{'gifwidth'}\"";
		} if($set{'gifheight'}){
			print " height=\"$set{'gifheight'}\"";
		}
		print ">\n"
	}
	print "<BR>\n<BR>\n"
		. "$daydat[2]\n<BR><BR>\n";
} else{
	print "この日の日記はありません";
}
print "</TD>\n"
	. "</TR>\n"
	. "</TBODY>\n</TABLE>\n"
	. "</TD>\n"
	. "<TR>\n"
	. "<TD colspan=\"2\" align=center><BR><A href=\"http://cgi-garage.parallel.jp\">CGI-GARAGE</A></TD>\n"
	. "</TR>\n</TBODY>\n</TABLE>\n"
	. "</CENTER>\n"
	. "</BODY>\n</HTML>\n";
exit;
1;

################################################################
sub calendarprint{
	my $before = $cgi->param('beforemonth');
	my $after = $cgi->param('aftermonth');
	my $text = $cgi->param('text');

	my @weekday = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
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
	if($text){
		my $textyear = $cgi->param('textyear');
		my $textmonth = $cgi->param('textmonth');
		jcode::tr(\$textyear, $zenkaku, $hankaku); jcode::tr(\$textmonth, $zenkaku, $hankaku);

		$form_year = $textyear;
		$form_month = $textmonth;
	}
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
	if(($realyear . sprintf("%02d",$realmonth) eq $form_year . sprintf("%02d",$form_month)) && $link eq ""){
		$form_day = "";
	} elsif(($realyear . sprintf("%02d",$realmonth) > $form_year . sprintf("%02d",$form_month)) && $link eq "" && $form_year && $form_month){
		$form_day = $monthdayArray[$form_month - 1];
	} elsif(($realyear . sprintf("%02d",$realmonth) < $form_year . sprintf("%02d",$form_month)) && $link eq ""){
		$form_day = 1;
	}

	if($form_year ne ""){
		$realyear = $form_year;
	} if($form_month ne ""){
		$realmonth = $form_month;
	} if($form_day){
		$realday = $form_day;
	}
	if((($realyear%4 == 0) && ($realyear%100 != 0)) || ($realyear%400 == 0)){$monthdayArray[1] = 29;}# 閏年の計算

	my $file = "./data/" . $realyear . sprintf("%02d",$realmonth) . ".cgi";
	my @data;
	if(-e $file){
		@data = &setread2($file);
	}
	my $daydat;
	my $daydat2 = $realyear . sprintf("%02d",$realmonth) . sprintf("%02d",$realday);
	for my $p(@data){
		my @p =split(/\t/,$p);
		if($p[0] eq $daydat2){
			$daydat = $p;
			next;
		}
	}

#####　今月1日の曜日　#####
	my $m = $realmonth;
	my $y = $realyear;
	if ($m < 3) { --$y; $m += 12; }# ツェラー公式
	my $weekday = int(($y+int($y/4) - int($y/100) + int($y/400) + int((13*$m+8)/5) + 1) % 7);


#####　今月の日数　######
	my $endday = $monthdayArray[$realmonth-1];

	my $cellprint = "<FORM ACTION=\"diary.cgi\" METHOD=POST>\n"
				  . "<input type=text name=textyear size=6>年"
				  . "<input type=text name=textmonth size=4>月<BR>"
				  . "<input type=submit name=text value=\"年月指定\"><BR><BR>"
				  . "<input type=submit name=\"beforemonth\" value=\"←前の月\"> 　 \n"
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
		my $days = $realyear . sprintf("%02d",$realmonth) . sprintf("%02d",$i);
		my $frag = 0;
		for my $p(@data){
			my @p =split(/\t/,$p);
			if($p[0] eq $days){
				$frag++;
				next;
			}
		}
		if($frag eq 0){
			$cellprint .= "$i</FONT></TD>\n";
		} else{
			$cellprint .= "<A href=diary.cgi?year=$realyear&month=$realmonth&day=$i&link=aaa>$i</A></FONT></TD>\n";
		}
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

	$cellprint .= "</TBODY>\n</TABLE>\n"
				. "<INPUT type=\"hidden\" name=\"year\" value=\"$realyear\">\n"
				. "<INPUT type=\"hidden\" name=\"month\" value=\"$realmonth\">\n"
				. "<INPUT type=\"hidden\" name=\"day\" value=\"$realday\">\n</FORM>\n";
	return($daydat,$cellprint);
}

sub readtemp{
	my($template) = @_;
	open(DAT,"<$template")||die print "Content-type: text/html\n\ntemplateData Open Error!<BR>テンプレートファイルが開けません。->$template";exit;

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
		print "Content-type: text/html\n\nflock Error!<BR>ファイルロックが使えません。";
		close(DAT);
		exit;
		}
}

sub setread(){
	my ($setdat) = @_;
	my %data = ();
	open(LOGS,"<$setdat")||die print "Content-type:text/html\n\n<BR>file open error!<BR>設定ファイルが開けません。ファイルが存在するか、ファイルのパーミッションを確認してください。->$setdat";
	&file_lock(*LOGS);
	while(my $line = <LOGS>){
		chomp($line);
		if($line =~ /^([a-zA-Z0-9\_\-]+)\=(.+)$/) {
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

	open(LOGS,"<$setdat")||die print "Content-type:text/html\n\n\n<BR>file open error!<BR>設定ファイルが開けません。ファイルが存在するか、ファイルのパーミッションを確認してください。->$setdat";
	&file_lock(*LOGS);
	while(my $line = <LOGS>){
		chomp($line);
		push(@data,$line);
	}
	close(LOGS);
	return @data;
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
