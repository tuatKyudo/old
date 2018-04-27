### ��˥塼/����
sub menu_rawlog {
	$i = 0;
	foreach (@filename) {
		if ($i == 0) { print"\t<TR${tbc[6]}>"; }
		print qq(<TD><A HREF="#rawlog_$_">$_</A></TD>);
		$i++;
		if ($i == $colspan) { print "</TR>\n"; $i = 0; }
	}
	# ;�ä����ڡ����򤴤ޤ���
	for (; $i < $colspan ; $i++) { print "<TD>��</TD>"; }
	print "</TR>\n";
}

### ��˥塼/������ȷ�
sub menu_count { print "\t<TR${tbc[6]}><TD><A HREF=\"#hour\">�����̽���</A></TD><TD><A HREF=\"#day\">���̽���</A></TD><TD><A HREF=\"#week\">�����̽���</A></TD><TD><A HREF=\"#weekly\">���̽���</A></TD><TD><A HREF=\"#month\">���̽���</A></TD><TD><A HREF=\"#year\">ǯ���̽���</A></TD></TR>\n"; }

### ��˥塼/��󥭥�
sub menu_rank { print "\t<TR${tbc[6]}><TH colspan=${colspan}><A HREF=\"#rank\">�Ƽ��󥭥�</A></TH></TR>\n"; }

### ��˥塼/���ȸ���
sub menu_ref {
print "\t<TR${tbc[6]}><TD><A HREF=\"#ref\">���ȸ�����</A></TD><TD><A HREF=\"#ref_own\">�����԰�ưʬ��</A></TD><TD>��</TD><TD>��</TD><TD>��</TD><TD>��</TD></TR>\n";
print "\t<TR${tbc[6]}><TD><A HREF=\"#search_share\">���������󥸥�Υ�����</A></TD><TD><A HREF=\"#search_key\">���������󥸥�ʬ��</A></TD><TD><A HREF=\"#tinami\">TINAMIʬ��</A></TD><TD><A HREF=\"#sp\">Surfers Paradiceʬ��</A></TD><TD>��</TD><TD>��</TD></TR>\n";
}

### ��˥塼/�ۥ��ȷ�
sub menu_host { print "\t<TR${tbc[6]}><TD><A HREF=\"#host\">�ۥ�������</A></TD><TD><A HREF=\"#domain\">����������</A></TD><TD><A HREF=\"#jp\">����ɥᥤ������</A></TD><TD><A HREF=\"#us\">�ƹ�ɥᥤ������</A></TD><TD>��</TD><TD>��</TD></TR>\n"; }

### ��˥塼/�֥饦����
sub menu_ua { print "\t<TR${tbc[6]}><TD><A HREF=\"#ua\">�֥饦������</A></TD><TD><A HREF=\"#share_ie\">IEƱ�ΤΥ�����</A></TD><TD><A HREF=\"#share_nn\">NNƱ�ΤΥ�����</A></TD><TD><A HREF=\"#share_os\">����OS����</A></TD><TD>��</TD><TD>��</TD></TR>\n"; }

### ��˥塼/���̾����
sub menu_screen { print "\t<TR${tbc[6]}><TD><A HREF=\"#screen\">���̾�������</A></TD><TD><A HREF=\"#screen_size\">������������</A></TD><TD><A HREF=\"#screen_color\">������������</A></TD><TD>��</TD><TD>��</TD><TD>��</TD></TR>\n"; }


;### HTML Ƭ����ʬ
sub html_head {
print <<"END";
Content-type: text/html

<HTML>
<HEAD>
	<META http-equiv=\"Content-Type\" content=\"text/html; charset=EUC-JP\">
	<META http-equiv=\"Content-Style-Type\" content=\"text/css\">

	<!-- efStat $ver  by Enogu Fukashigi (http://yugen.main.jp/) -->
	<!-- ���Υ�����ץȤκǿ��Ǥ��ߤ������Ͼ嵭���ɥ쥹�ޤǤ��ۤ�������(^^) -->

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


;### HTML ���äݤ���ʬ
sub html_tail {
	print "\n<HR>\n<DIV align=right><A href=\"http://yugen.main.jp/\">[efStat $ver] / &copy;1998-2001 Enogu Fukashigi\@YugenKoubou</A></DIV>\n</BODY>\n</HTML>\n";
}


package func;
;#+------------------------------------------------------------------------
;#|efStat
;#|���Ѵؿ�
;#+------------------------------------------------------------------------
### �ơ��֥���ɤ߹���
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

;### ���׷�̤�ꥹ�Ȥˤ���ؿ�
;### ɽ�����¤�Ϣ��������������ȹ߽�˥����Ȥ���������֤�
;### $assoc_array = Ϣ������ؤΥ�ե���� (��Ȥϥ�����Υ�����ȿ�)
;### $limit       = �������¤ؤΥ�ե���� (���ο��򲼲��ʬ�ϥꥹ�Ȥ����ڤ�ΤƤ�)
sub MakeList {
	my ($hash, $limit) = @_;
	my (@array, $key, $value);

	foreach $key (sort({$$hash{$b} <=> $$hash{$a}} keys(%$hash))) {
		push(@array, "$$hash{$key}\t$key") if ($$limit < $$hash{$key});
	}

	return @array;
}


;### �����������ä�������������ȹ���ͤ��֤��ؿ�
sub CalcSum {
	my $sum;
	foreach (@_) { $sum += $_; }
	return $sum;
}


;### 62�ʿ���10�ʿ�
sub C62_Decode {
	my $str = reverse($_[0]);
	my($digit, $i);

	for ($i = 0; $i < length($str); $i++) {
		$digit += index('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', substr($str, $i, 1)) * (62 ** $i);
	}

	return $digit;
}


;### 10�ʿ���62�ʿ�
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


;### ���顼����
sub PutError {
	my($mesg) = @_;
	$html_title = '�۾ｪλ���ޤ���';
	&main::html_head;
	print "<CENTER><P><B>[���顼]</B>$mesg</P></CENTER>\n";
	&main::html_tail;
	exit(1);
}


;### URL���16��ɽ����ʸ�����᤹�ؿ�(URL�ǥ�����)
sub URLdecode {
	my($str) = @_;
	$str =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack("C",hex($1))/ge;
	return $str;
}


;### URL��δ�������16��ɽ���ˤ���ؿ�(URL���󥳡���)
sub URLencode {
	my($str) = @_;
	$str =~ s/([^\x21-\x24\x26-\x7E])/sprintf("%%%02X",unpack("C",$1))/ge;
	return $str;
}

;### ��󥯤Υ�������ؿ�(URL����������ʸ���������Ѵ���URL�ʤ����"-"���֤�)
;### $mode��1,2�λ� ?(���ޥ�ɥ��ѥ졼����) ���褿����Ԥ��ղä���
sub MakeLink {
	my($ref,$mode) = @_;
	my($work);

	$work =  &URLdecode($ref);
	$work =~ s/&/&amp;/g;
	$work =~ s/</&lt;/g;
	$work =~ s/>/&gt;/g;
	$work =~ s/"/&quot;/g;
	$work =~ s/\?/<BR>\?/g if ($mode == 1);	# ���ȸ���
	$work =~ s/\?/\n\t\?/g if ($mode == 2);	# ������
	return "<A HREF=\"$ref\">$work</A>";
}

;### �̻��ä�������������ؿ�
;### (�̻���(1970/01/01 00:00:00����)����������[ǯ/��/��/(��) ��:ʬ:��]��ʸ��������������֤�)
sub MakeDate {
	my($t) = @_;
	my(@wdays, $sec, $min, $hour, $day, $mon, $year, $wday);
	@wdays=('��','��','��','��','��','��','��');
	($sec,$min,$hour,$day,$mon,$year,$wday) = localtime($t);
	return sprintf("%d/%02d/%02d(%s) %02d:%02d:%02d",1900+$year,$mon+1,$day,$wdays[$wday],$hour,$min,$sec);
}

### GMT�����ǻ�����֤��ؿ�
sub GmtDate {
	my($t) = @_;
	my($sec, $min, $hour, $day, $mon, $year, $wday, @wdays, @month);
	@wdays = ('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat');
	@month = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec');

	($sec,$min,$hour,$day,$mon,$year,$wday) = gmtime($t);
	return sprintf("%s, %02d %s %04d %02d:%02d:%02d GMT", $wdays[$wday], $day, $month[$mon], $year+1900, $hour, $min, $sec);
}


1;
