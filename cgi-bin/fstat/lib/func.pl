### メニュー/生ログ
sub menu_rawlog {
	$i = 0;
	foreach (@filename) {
		if ($i == 0) { print"\t<TR${tbc[6]}>"; }
		print qq(<TD><A HREF="#rawlog_$_">$_</A></TD>);
		$i++;
		if ($i == $colspan) { print "</TR>\n"; $i = 0; }
	}
	# 余ったスペースをごまかす
	for (; $i < $colspan ; $i++) { print "<TD>　</TD>"; }
	print "</TR>\n";
}

### メニュー/カウント系
sub menu_count { print "\t<TR${tbc[6]}><TD><A HREF=\"#hour\">時間別集計</A></TD><TD><A HREF=\"#day\">日別集計</A></TD><TD><A HREF=\"#week\">曜日別集計</A></TD><TD><A HREF=\"#weekly\">週別集計</A></TD><TD><A HREF=\"#month\">月別集計</A></TD><TD><A HREF=\"#year\">年度別集計</A></TD></TR>\n"; }

### メニュー/ランキング
sub menu_rank { print "\t<TR${tbc[6]}><TH colspan=${colspan}><A HREF=\"#rank\">各種ランキング</A></TH></TR>\n"; }

### メニュー/参照元系
sub menu_ref {
print "\t<TR${tbc[6]}><TD><A HREF=\"#ref\">参照元統計</A></TD><TD><A HREF=\"#ref_own\">閲覧者移動分析</A></TD><TD>　</TD><TD>　</TD><TD>　</TD><TD>　</TD></TR>\n";
print "\t<TR${tbc[6]}><TD><A HREF=\"#search_share\">サーチエンジンのシェア</A></TD><TD><A HREF=\"#search_key\">サーチエンジン分析</A></TD><TD><A HREF=\"#tinami\">TINAMI分析</A></TD><TD><A HREF=\"#sp\">Surfers Paradice分析</A></TD><TD>　</TD><TD>　</TD></TR>\n";
}

### メニュー/ホスト系
sub menu_host { print "\t<TR${tbc[6]}><TD><A HREF=\"#host\">ホスト統計</A></TD><TD><A HREF=\"#domain\">国籍別統計</A></TD><TD><A HREF=\"#jp\">国内ドメイン統計</A></TD><TD><A HREF=\"#us\">米国ドメイン統計</A></TD><TD>　</TD><TD>　</TD></TR>\n"; }

### メニュー/ブラウザ系
sub menu_ua { print "\t<TR${tbc[6]}><TD><A HREF=\"#ua\">ブラウザ統計</A></TD><TD><A HREF=\"#share_ie\">IE同士のシェア</A></TD><TD><A HREF=\"#share_nn\">NN同士のシェア</A></TD><TD><A HREF=\"#share_os\">利用OS統計</A></TD><TD>　</TD><TD>　</TD></TR>\n"; }

### メニュー/画面情報系
sub menu_screen { print "\t<TR${tbc[6]}><TD><A HREF=\"#screen\">画面情報統計</A></TD><TD><A HREF=\"#screen_size\">サイズ別統計</A></TD><TD><A HREF=\"#screen_color\">色深度別統計</A></TD><TD>　</TD><TD>　</TD><TD>　</TD></TR>\n"; }


;### HTML 頭の部分
sub html_head {
print <<"END";
Content-type: text/html

<HTML>
<HEAD>
	<META http-equiv=\"Content-Type\" content=\"text/html; charset=EUC-JP\">
	<META http-equiv=\"Content-Style-Type\" content=\"text/css\">

	<!-- efStat $ver  by Enogu Fukashigi (http://yugen.main.jp/) -->
	<!-- このスクリプトの最新版が欲しい方は上記アドレスまでお越し下さい(^^) -->

	<TITLE>efStat / $html_title</TITLE>

	<STYLE type=\"text/css\"><!--
		BODY    {font-family:Arial,Verdana;}
		A       {text-decoration:none; font-weight:bold}
		A:hover {text-decoration: underline}
	--></STYLE>
</HEAD>

$html_body

<BASEFONT size=3>

<B><FONT size=\"+3\">efStat </FONT><FONT size=\"+1\">Ver.$ver</FONT></B>
<HR>

END
}


;### HTML しっぽの部分
sub html_tail {
	print "\n<HR>\n<DIV align=right><A href=\"http://yugen.main.jp/\">[efStat $ver] / &copy;1998-2001 Enogu Fukashigi\@YugenKoubou</A></DIV>\n</BODY>\n</HTML>\n";
}


package func;
;#+------------------------------------------------------------------------
;#|efStat
;#|共用関数
;#+------------------------------------------------------------------------
### テーブルを読み込む
sub LoadTable {
	my($filename) = @_;
	my(%hash);

	open(TBL, $filename) || die "Couldn't open";
	while (<TBL>) {
		chomp;
		next if /^#/;
		next unless /^([^\t]*)\t+(.*)$/;
		$hash{"$1"} = "$2";
	}

	return \%hash;
}

;### 統計結果をリストにする関数
;### 表示下限と連想配列を放り込むと降順にソートした配列を返す
;### $assoc_array = 連想配列へのリファレンス (中身はキー毎のカウント数)
;### $limit       = 作成下限へのリファレンス (この数を下回る分はリストから切り捨てる)
sub MakeList {
	my ($hash, $limit) = @_;
	my (@array, $key, $value);

	foreach $key (sort({$$hash{$b} <=> $$hash{$a}} keys(%$hash))) {
		push(@array, "$$hash{$key}\t$key") if ($$limit < $$hash{$key});
	}

	return @array;
}


;### 自然数の入った配列を放り込むと合計値を返す関数
sub CalcSum {
	my $sum;
	foreach (@_) { $sum += $_; }
	return $sum;
}


;### 62進数→10進数
sub C62_Decode {
	my $str = reverse($_[0]);
	my($digit, $i);

	for ($i = 0; $i < length($str); $i++) {
		$digit += index('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', substr($str, $i, 1)) * (62 ** $i);
	}

	return $digit;
}


;### 10進数→62進数
sub C62_Encode {
	my($digit) = $_[0];
	my($str);

	if (!$digit) {
		return 0;
	} else {
		while ($digit) {
			$str .= substr('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', ($digit % 62), 1);
			$digit = int($digit / 62);
		}
		return reverse($str);
	}
}


;### エラー出力
sub PutError {
	my($mesg) = @_;
	$html_title = '異常終了しました';
	&main::html_head;
	print "<CENTER><P><B>[エラー]</B>$mesg</P></CENTER>\n";
	&main::html_tail;
	exit(1);
}


;### URL内の16進表記を文字に戻す関数(URLデコード)
sub URLdecode {
	my($str) = @_;
	$str =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack("C",hex($1))/ge;
	return $str;
}


;### URL内の漢字等を16進表記にする関数(URLエンコード)
sub URLencode {
	my($str) = @_;
	$str =~ s/([^\x21-\x24\x26-\x7E])/sprintf("%%%02X",unpack("C",$1))/ge;
	return $str;
}

;### リンクのタグを作る関数(URLを放り込むと文字コード変換、URLなければ"-"を返す)
;### $modeが1,2の時 ?(コマンドセパレータ？) が来たら改行を付加する
sub MakeLink {
	my($ref,$mode) = @_;
	my($work);

	$work =  &URLdecode($ref);
	$work =~ s/&/&amp;/g;
	$work =~ s/</&lt;/g;
	$work =~ s/>/&gt;/g;
	$work =~ s/"/&quot;/g;
	$work =~ s/\?/<BR>\?/g if ($mode == 1);	# 参照元用
	$work =~ s/\?/\n\t\?/g if ($mode == 2);	# 生ログ用
	return "<A HREF=\"$ref\">$work</A>";
}

;### 通算秒から日時を得る関数
;### (通算秒(1970/01/01 00:00:00から)を放り込むと[年/月/日/(曜) 時:分:秒]の文字列に整形して返す)
sub MakeDate {
	my($t) = @_;
	my(@wdays, $sec, $min, $hour, $day, $mon, $year, $wday);
	@wdays=('日','月','火','水','木','金','土');
	($sec,$min,$hour,$day,$mon,$year,$wday) = localtime($t);
	return sprintf("%d/%02d/%02d(%s) %02d:%02d:%02d",1900+$year,$mon+1,$day,$wdays[$wday],$hour,$min,$sec);
}

### GMT形式で時刻を返す関数
sub GmtDate {
	my($t) = @_;
	my($sec, $min, $hour, $day, $mon, $year, $wday, @wdays, @month);
	@wdays = ('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat');
	@month = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec');

	($sec,$min,$hour,$day,$mon,$year,$wday) = gmtime($t);
	return sprintf("%s, %02d %s %04d %02d:%02d:%02d GMT", $wdays[$wday], $day, $month[$mon], $year+1900, $hour, $min, $sec);
}


1;
