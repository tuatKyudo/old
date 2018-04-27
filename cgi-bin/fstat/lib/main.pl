;#+------------------------------------------------------------------------
;#|efStat
;#|�����ϥ롼����
;#+------------------------------------------------------------------------

if (($P{PASS} ne $Pass) && ($DoPass)) {
	print "<CENTER><P><B>[���顼]</B>�ѥ���ɤ����פ��ޤ���Ǥ�����</P></CENTER>\n";
	&html_tail;
	exit(1);
}


;### �׻�����¬�곫��
$CPU_start = (times)[0] if ($DoPutBenchmark);

### �������Ѵ��ѥơ��֥���ɤ߹���
$TABLE{'agent'}    = &func::LoadTable('./lib/table/agent.tbl');
$TABLE{'cctld'}    = &func::LoadTable('./lib/table/cctld.tbl');
$TABLE{'gtld'}     = &func::LoadTable('./lib/table/gtld.tbl');
$TABLE{'jpdomain'} = &func::LoadTable('./lib/table/jpdomain.tbl');
$TABLE{'tinami'}   = &func::LoadTable('./lib/table/tinami.tbl');

foreach $filename (@filename) {
	if ($filename eq '') { next; }		# ".log"�ե������к�
	
	### �ե�����򥪡��ץ�
	unless (open(LOG,"<${Dir_Log}${filename}.log")) {
		print "<CENTER><P><B>[���顼]</B>���������� ( ${Dir_Log}${filename}.log ) �򳫤����Ȥ��Ǥ��ޤ���<BR>���Υե������������¸�ߤ��Ƥ��뤫���ѡ��ߥå������������� (606����666) �ʤɤ��ǧ��������</P></CENTER>\n";
		&html_tail;
		exit(1);
	}
	flock(LOG,2);

	### �ץ����¹Ի�������
	($SEC,$MIN,$HOUR,$DAY,$MON,$YEAR,$YOUBI,$TOTAL) = localtime(time);

	### �إå������ɤ߹���������å�
	chop($HEAD = <LOG>);
	($LOG_ID, $LOG_SINCE{$filename}) = split(/\t/, $HEAD);
	$LOG_SINCE{$filename} = &func::C62_Decode($LOG_SINCE{$filename});

	if ($LOG_ID ne 'FC2') { next; }

	### �Ƽ����
	chomp($INFO{$filename} = <LOG>);
	$RANK_ALL{$filename} = &func::C62_Decode((split(/\t/, $INFO{$filename}))[1]);

	### ���̽���
	chomp($DAY{$filename} = <LOG>);
	$RANK_DAY{$filename} = &func::C62_Decode((split(/\t/, $DAY{$filename}))[0]);

	### �����̽���
	chomp($HOUR{$filename} = <LOG>);

	### �����̽���
	chomp($WEEK{$filename} = <LOG>);

	### ���̽���
	chomp($WEEKLY{$filename} = <LOG>);
	$RANK_WEEKLY{$filename} = &func::C62_Decode((split(/\t/, $WEEKLY{$filename}))[0]);

	### ���̽���
	chomp($MONTH{$filename} = <LOG>);
	$RANK_MONTH{$filename} = &func::C62_Decode((split(/\t/, $MONTH{$filename}))[$MON]);

	### ǯ���̽���
	chomp($YEAR{$filename} = <LOG>);
	# $RANK_YEAR{$filename} = &func::C62_Decode((split(/\t/, $YEAR{$filename}))[0]);

	### ��������������
	# �����ϰϤ����ꤵ��Ƥ�����
	if ((defined($P{'d'})) && ($P{'d'} ne 'a')) {
		if ($P{'d'} eq 'y') { $TOTAL = --$TOTAL; }
		@HOUR = ('0') x 24;
		while (chomp($LINE = <LOG>)) {
			&Macro_Split;
			($sec,$min,$hour,$day,$mon,$year,$youbi,$total) = localtime($date);
			if ($TOTAL eq $total) {
				++$HOUR[ $hour ];
				&Macro_ProcessLine;
			}
		}
		foreach (@HOUR) { $_ = &func::C62_Encode($_); }
		$HOUR{$filename} = join("\t", @HOUR);
	}

	# ����ɽ��
	else {
		while (chop($LINE = <LOG>)) {
			&Macro_Split;
			&Macro_ProcessLine;
		}
	}

	flock(LOG,8);
	close(LOG);

	### �����ѥ����󥿤��������Ƥ���
	$COUNT_RAWLOG = 0;

	### ˽���ɻ��ѥ�ߥå�
	if ($SAMPLES == $Limit_Analyzer) {
		print "<CENTER><P><B>[���顼]</B>�ݸǽ\��Ư�����ץ���������λ���ޤ�����<BR>$Limit_Analyzer��ޤǤΥ����������Ǥ��ʤ��褦�ˤʤäƤ��ޤ���<BR>���ϡ��ץ���ब˽\�����ޤ��������������Ǥ��Τǡ����Һ�Ԥˤ�Ϣ��������</P></CENTER>\n";
		&html_tail;
		exit(1);
	}
}


sub Macro_Split {
	($num, $date, $host, $agent, $ref, $screen) = split(/\t/, $LINE);
	$num  = &func::C62_Decode($num);
	$date = &func::C62_Decode($date);

	$host =~ tr/A-Z/a-z/;

	$ref  = &func::URLdecode($ref);
	&jcode::convert(\$ref, 'euc', '', 'z');
	&jcode::tr(\$ref, '��-����-�ڣ�-����', '0-9a-za-z ');
	$ref = &func::URLencode($ref);
}

sub Macro_ProcessLine {
	### ���ֿ��������ε�Ͽ����
	$now = $date if ($SAMPLES == 0);

	### ���������
	if (($P{MODE} eq 'rawlog') || ($P{MODE} eq 'all') || ($P{MODE} eq 'solo_rawlog') || ($P{MODE} eq 'solo_all')) {
		&Macro_CountRawlog() if ($COUNT_RAWLOG < $Limit_Log);
	}

	### ���ȸ�����, TINAMI���ƥ���ʬ��, Surfers Paradiceʬ��
	&Macro_CountRef() if (($P{MODE} eq 'ref') || ($P{MODE} eq 'all') || ($P{MODE} eq 'solo_analyze') || ($P{MODE} eq 'solo_all'));

	### �ۥ���̾����, ����ʬ��, ����ɥᥤ��ʬ��
	&Macro_CountHost() if (($P{MODE} eq 'host') || ($P{MODE} eq 'all') || ($P{MODE} eq 'solo_analyze') || ($P{MODE} eq 'solo_all'));

	### �֥饦������, �֥饦��ʬ��, �����꡼�����
	&Macro_CountAgent() if (($P{MODE} eq 'ua') || ($P{MODE} eq 'all') || ($P{MODE} eq 'solo_analyze') || ($P{MODE} eq 'solo_all'));

	### �����꡼�����
	&Macro_CountScreen() if (($P{MODE} eq 'screen') || ($P{MODE} eq 'all') || ($P{MODE} eq 'solo_analyze') || ($P{MODE} eq 'solo_all'));

	### ����ץ�󥰤������������������
	$SAMPLES++;

	### ���ָŤ����ε�Ͽ����
	$old = $date;
}


### ���׷�̤򥽡���
### Ϣ�����������������ɬ�פʾ�������򤷤Ƥ���
### ���פˤʤä�Ϣ�������������
if (($P{MODE} eq 'count') || ($P{MODE} eq 'all')) {
	#����󥭥�
	@rank_all			= &func::MakeList(\%RANK_ALL, \0);
	$COUNT_ALL			= &func::CalcSum(values(%RANK_ALL));
	undef %RANK_ALL;

	#��֥�󥭥�
	@rank_month			= &func::MakeList(\%RANK_MONTH, \0);
	$COUNT_MONTH		= &func::CalcSum(values(%RANK_MONTH));
	undef %RANK_MONTH;

	#���֥�󥭥�
	@rank_weekly		= &func::MakeList(\%RANK_WEEKLY, \0);
	$COUNT_WEEKLY		= &func::CalcSum(values(%RANK_WEEKLY));
	undef %RANK_WEEKLY;

	#������󥭥�
	@rank_day			= &func::MakeList(\%RANK_DAY, \0);
	$COUNT_DAY			= &func::CalcSum(values(%RANK_DAY));
	undef %RANK_DAY;
}


if (($P{MODE} eq 'ref') || ($P{MODE} eq 'all') || ($P{MODE} eq 'solo_analyze') || ($P{MODE} eq 'solo_all')) {
	while (($key, $value) = each(%REF)) {
		foreach (@Complete_URL) {
			if ($key =~ /$$_[0]/) {
				$REF{"<B>[User]</B> $$_[1]"} += $value;
				delete $REF{$key};
				last;
			}
		}
	}

	@ref				= &func::MakeList(\%REF, \$Limit_Ref);
	$COUNT_REF			= &func::CalcSum(values(%REF));					#���������⻲�ȿ�
	undef %REF;

	@ref_own			= &func::MakeList(\%REF_OWN, \0);
	$COUNT_OWN			= &func::CalcSum(values(%REF_OWN));				#���������⻲�ȿ�
	undef %REF_OWN;

	@ref_search			= &func::MakeList(\%REF_SEARCH, \$Limit_Search);
	$COUNT_SEARCH		= &func::CalcSum(values(%REF_SEARCH));			#���������󥸥�Υ���������
	undef %REF_SEARCH;

	#���������󥸥󤫤��褿��
	@ref_search_share	= &func::MakeList(\%REF_SEARCH_SHARE, \0);
	$COUNT_SEARCH_SHARE	= &func::CalcSum(values(%REF_SEARCH_SHARE));	
	$COUNT_TN_			= $REF_SEARCH_SHARE{'TINAMI'};					#TINAMI�����褿��
	$COUNT_SP_			= $REF_SEARCH_SHARE{'Surfers Paradice'};		#SP�����褿��
	undef %REF_SEARCH_SHARE;

	@ref_tinami			= &func::MakeList(\%REF_TINAMI, \$Limit_Tinami);
	$COUNT_TN			= &func::CalcSum(values(%REF_TINAMI));			#TINAMI�Υ���������
	undef %REF_TINAMI;

	@ref_sp				= &func::MakeList(\%REF_SP, \$Limit_Sp);
	$COUNT_SP			= &func::CalcSum(values(%REF_SP));				#SP�Υ���������
	undef %REF_SP;
}


if (($P{MODE} eq 'host') || ($P{MODE} eq 'all') || ($P{MODE} eq 'solo_analyze') || ($P{MODE} eq 'solo_all')) {
	@host				= &func::MakeList(\%HOST, \$Limit_Host);
	undef %HOST;

	@host_dm			= &func::MakeList(\%HOST_DM, \$Limit_Domain);
	$COUNT_JP			= $HOST_DM{'jp'};
	$COUNT_US			= $HOST_DM{'us'};
	undef %HOST_DM;

	@host_dm_jp			= &func::MakeList(\%HOST_DM_JP, \$Limit_Jp);
	undef %HOST_DM_JP;

	@host_dm_us			= &func::MakeList(\%HOST_DM_US, \$Limit_Us);
	undef %HOST_DM_US;
}


if (($P{MODE} eq 'ua') || ($P{MODE} eq 'all') || ($P{MODE} eq 'solo_analyze') || ($P{MODE} eq 'solo_all')) {
	@agent				= &func::MakeList(\%AGENT, \$Limit_Agent);
	undef %AGENT;

	@agent_ie			= &func::MakeList(\%AGENT_IE, \0);
	$COUNT_IE			= &func::CalcSum(values(%AGENT_IE));			#IE�Υ�����
	undef %AGENT_IE;

	@agent_nn			= &func::MakeList(\%AGENT_NN, \0);
	$COUNT_NN			= &func::CalcSum(values(%AGENT_NN));			#NN�Υ�����
	undef %AGENT_NN;

	@agent_os			= &func::MakeList(\%AGENT_OS, \0);
	$COUNT_OS			= &func::CalcSum(values(%AGENT_OS));			#OS�Υ�����
	undef %AGENT_OS;
}


if (($P{MODE} eq 'screen') || ($P{MODE} eq 'all') || ($P{MODE} eq 'solo_analyze') || ($P{MODE} eq 'solo_all')) {
	@screen				= &func::MakeList(\%SCREEN, \0);
	$COUNT_SCREEN		= &func::CalcSum(values(%SCREEN));				#ͭ�դʲ��̾��󥫥���ȿ�
	undef %SCREEN;

	@screen_size		= &func::MakeList(\%SCREEN_SIZE, \0);
	$COUNT_SCREEN_SIZE	= &func::CalcSum(values(%SCREEN_SIZE));			#ͭ�դʲ��̾��󥫥���ȿ�
	undef %SCREEN_SIZE;

	@screen_color		= &func::MakeList(\%SCREEN_COLOR, \0);
	$COUNT_SCREEN_COLOR	= &func::CalcSum(values(%SCREEN_COLOR));		#ͭ�դʲ��̾��󥫥���ȿ�
	undef %SCREEN_COLOR;
}



### �����ɤ䵭����̣����ʸ������Ѵ�����
&Macro_ChangeList;


### �Ƽ����
if (($P{MODE} eq 'solo_rawlog') || ($P{MODE} eq 'solo_analyze') || ($P{MODE} eq 'solo_all')) {
	$days = ($now-$old)/86400;						#�����ä�����(����)
	$now = &func::MakeDate($now);
	$old = &func::MakeDate($old);

	print "<CENTER><TABLE BORDER=2 CELLSPACING=0 CELLPADDING=2>\n";
	print "\t<TR><TH COLSPAN=4${tbc[0]}>�оݥ��ե����� : ${filename[0]}.log</TH></TR>\n";
	print "\t<TR><TH${tbc[1]}>Ĵ������</TH><TD${tbc[5]}>$old �� $now</TD><TH${tbc[2]}>��ҥåȿ�</TH><TD${tbc[6]}>$RANK_ALL{ $filename[0] }</TD></TR>\n";

	if ($days > 0) {
		$ave  = sprintf("%0.2f", $SAMPLES/$days);
		$days = sprintf("%0.2f", $days);
		print "\t<TR><TH COLSPAN=4${tbc[8]}>$SAMPLES��������ã����$days���פ��ޤ���(1��ʿ�� $ave ��������)</TH></TR>\n";
	}
	print "</TABLE></CENTER><HR>\n\n";
}


### ����˥塼
unless ($P{MODE} eq 'solo_rawlog') {
	### ��˥塼
	$colspan = 6;		# ��ο�
	print "<!-- ����˥塼 -->\n<A name=menu></A>\n<CENTER><TABLE border=1 cellspacing=0 cellpadding=1${tbc[0]}>\n\t<TR><TH colspan=${colspan}><FONT size=+1>�� ����˥塼 ��</FONT></TH></TR>\n";

	if ($P{MODE} eq 'rawlog') {
		&menu_rawlog;
	} elsif ($P{MODE} eq 'count') {
		&menu_count;
		&menu_rank;
	} elsif ($P{MODE} eq 'ref') {
		&menu_ref;
	} elsif ($P{MODE} eq 'host') {
		&menu_host;
	} elsif ($P{MODE} eq 'ua') {
		&menu_ua;
	} elsif ($P{MODE} eq 'screen') {
		&menu_screen;
	} elsif ($P{MODE} eq 'all') {
		print "\t<TR><TH colspan=${colspan}${tbc[0]}>��������</TH></TR>\n";
		&menu_rawlog;
		print "\t<TR><TH colspan=${colspan}${tbc[0]}>������¾���ע�</TH></TR>\n";
		&menu_count;
		&menu_rank;
		&menu_ref;
		&menu_host;
		&menu_ua;
		&menu_screen;
	} elsif (($P{MODE} eq 'solo_analyze') || ($P{MODE} eq 'solo_all')) {
		&menu_count;
		&menu_ref;
		&menu_host;
		&menu_ua;
		&menu_screen;
	}
	print "<TR><TD colspan=${colspan}><DIV ALIGN=right><A HREF=\"$self\">[�� ��˥塼�����]</A></DIV></TD></TR></TABLE></CENTER><HR>\n\n";
}


### ����
if (($P{MODE} eq 'rawlog') || ($P{MODE} eq 'all') || ($P{MODE} eq 'solo_rawlog') || ($P{MODE} eq 'solo_all')) {
	### �����Υơ��֥�
	print "<CENTER>\n";
	foreach $filename (@filename) {
		if (defined($RAWLOG{$filename})) {
			print "<A NAME=rawlog_${filename}></A>\n<TABLE border=1 cellspacing=0 cellpadding=1${tbc[0]}><TR><TD><A HREF=\"#menu\"><B><FONT size=+1>���� ($filename.log)</FONT> / �ǿ�$Limit_Log��</B></A></TD></TR><TR><TD><PRE>\n";
			print $RAWLOG{$filename};
			print "</PRE></TD></TR></TABLE><BR>\n";
		}
	}
	print "</CENTER>\n";
}


### ������Ƚ���
if (($P{MODE} eq 'count') || ($P{MODE} eq 'all') || ($P{MODE} eq 'solo_analyze') || ($P{MODE} eq 'solo_all')) {
	print "<!-- ������ȿ����� -->\n<CENTER>\n";
	print "<!-- ���̽��� -->\n<A name=day></A>\n";

	&Macro_PutTable_b(0, $koumoku{'day'}, \%DAY);
	undef %DAY;
	print "\n\n<BR>\n\n";
	print "<!-- ���̽��� -->\n<A name=weekly></A>\n";
	&Macro_PutTable_b(0, $koumoku{'weekly'}, \%WEEKLY);
	undef %WEEKLY;
	print "\n\n<BR>\n\n";
	print "<!-- ���̽��� -->\n<A name=month></A>\n";
	&Macro_PutTable_b(0, $koumoku{'month'}, \%MONTH);
	undef %MONTH;
	print "\n\n<BR>\n\n";
	print "<!-- �������̽��� -->\n<A name=hour></A>\n";
	&Macro_PutTable_b(2, $koumoku{'hour'}, \%HOUR);
	undef %HOUR;
	print "\n\n<BR>\n\n";
	print "<!-- �����̽��� -->\n<A name=week></A>\n";
	&Macro_PutTable_b(2, $koumoku{'week'}, \%WEEK);
	undef %WEEK;
	print "\n\n<BR>\n\n";
	print "<!-- ǯ���̽��� -->\n<A name=year></A>\n";
	&Macro_PutTable_b(0, $koumoku{'year'}, \%YEAR);
	undef %YEAR;
	print "\n</CENTER><BR>\n\n";

	unless (($P{MODE} eq 'solo_analyze') || ($P{MODE} eq 'solo_all')) {
		print "<!-- ���������󥭥� -->\n<A name=rank></A>\n<CENTER><TABLE border=0 cellpadding=4><TR><TD valign=top>\n";
		&Macro_PutTable_a(0, '����󥭥�', '�ڡ���̾', $COUNT_ALL,		'', 0, 0, \@rank_all);
		undef @rank_all;
		print "</TD><TD valign=top>\n";
		&Macro_PutTable_a(0, '��֥�󥭥�', '�ڡ���̾', $COUNT_MONTH,	'', 0, 0, \@rank_month);
		undef @rank_month;
		print "</TD></TR><TR><TD valign=top>\n";
		&Macro_PutTable_a(0, '���֥�󥭥�', '�ڡ���̾', $COUNT_WEEKLY,	'', 0, 0, \@rank_weekly);
		undef @rank_weekly;
		print "</TD><TD valign=top>\n";
		&Macro_PutTable_a(0, '������󥭥�', '�ڡ���̾', $COUNT_DAY,		'', 0, 0, \@rank_day);
		undef @rank_day;
		print "</TD></TR></TABLE></CENTER><BR>\n\n";
	}
}

### ���ȸ���
if (($P{MODE} eq 'ref') || ($P{MODE} eq 'all') || ($P{MODE} eq 'solo_analyze') || ($P{MODE} eq 'solo_all')) {
	print "<!-- ���ȸ� -->\n<A name=ref></A>\n<CENTER>\n";
	&Macro_PutTable_a(0, '���ȸ�����', '���ȸ�URL', $COUNT_REF, '', 0, $Limit_Ref, \@ref);
	undef @ref;
	print "</CENTER><BR>\n\n";
	print "<!-- ���������ưʬ�� -->\n<A name=ref_own></A><CENTER>\n";
	&Macro_PutTable_a(2, '���������ưʬ��', '��ư������', $COUNT_OWN, '���������⢪����������', $COUNT_OWN, 0, \@ref_own);
	undef @ref_own;
	print "</CENTER><BR>\n\n";

	print "<!-- ���������󥸥����� -->\n<CENTER><TABLE border=0 cellpadding=8><TR><TD valign=top>\n<A name=search_share></A>\n";
	&Macro_PutTable_a(2, '���������󥸥󥷥���', '̾��', $COUNT_SEARCH_SHARE, '���������󥸥󤫤�', $COUNT_SEARCH_SHARE, 0, \@ref_search_share);
	undef @ref_search_share;
	print "\n</TD><TD valign=top>\n<A name=search_key></A>\n";
	&Macro_PutTable_a(0, '���������󥸥�ʬ��', '�������(����)', $COUNT_SEARCH, '', 0, $Limit_Search, \@ref_search);
	undef @ref_search;
	print "\n</TD></TR></TABLE></CENTER>\n\n";
	print "<CENTER><TABLE border=0 cellpadding=8><TR><TD valign=top>\n<A name=tinami></A>\n";
	&Macro_PutTable_a(1, 'TINAMIʬ��', '�������', $COUNT_TN, 'TINAMI����', $COUNT_TN_, $Limit_Tinami, \@ref_tinami);
	undef @ref_tinami;
	print "\n</TD><TD valign=top>\n<A name=sp></A>\n";
	&Macro_PutTable_a(1, 'Surfers Paradiceʬ��', '�������', $COUNT_SP, 'SP����', $COUNT_SP_, $Limit_Sp, \@ref_sp);
	undef @ref_sp;
	print "\n</TD></TR></TABLE></CENTER><BR>\n\n";
}

### �ۥ��ȷ�
if (($P{MODE} eq 'host') || ($P{MODE} eq 'all') || ($P{MODE} eq 'solo_analyze') || ($P{MODE} eq 'solo_all')) {
	print "<!-- �ɥᥤ������ -->\n<CENTER><TABLE border=0 cellpadding=8><TR><TD valign=top>\n<A name=host></A>\n";
	&Macro_PutTable_a(0, '�ɥᥤ��������', '�ɥᥤ��', $SAMPLES, '', 0, $Limit_Host, \@host);
	undef @host;
	print "\n</TD><TD valign=top>\n<A name=domain></A>\n";
	&Macro_PutTable_a(0, '����������', '���� (ccTLD)', $SAMPLES, '', 0, $Limit_Domain, \@host_dm);
	undef @host_dm;
	print "\n\n<BR>\n\n<A name=jp></A>\n";
	&Macro_PutTable_a(2, '����ɥᥤ������', '��2��٥�ɥᥤ��', $COUNT_JP, '���ܤ���', $COUNT_JP, 0, \@host_dm_jp);
	undef @host_dm_jp;
	print "\n\n<BR>\n\n<A name=us></A>\n";
	&Macro_PutTable_a(2, '�ƹ�ɥᥤ������', '��°�ȿ� (gTLD)', $COUNT_US, '�ƹ񤫤�', $COUNT_US, 0, \@host_dm_us);
	undef @host_dm_us;
	print "\n</TD></TR></TABLE></CENTER><BR>\n\n";
}

### �֥饦����
if (($P{MODE} eq 'ua') || ($P{MODE} eq 'all') || ($P{MODE} eq 'solo_analyze') || ($P{MODE} eq 'solo_all')) {
	print "<!-- �֥饦������ -->\n<CENTER><TABLE border=0 cellpadding=8><TR><TD valign=top>\n<A name=ua></A>\n";
	&Macro_PutTable_a(0, '�֥饦������', '�����������̾��', $SAMPLES, '', 0, $Limit_Agent, \@agent);
	undef @agent;
	print "\n</TD><TD valign=top>\n<A name=share_ie></A>\n";
	&Macro_PutTable_a(2, 'IEƱ�ΤΥ�����', 'IE�С������', $COUNT_IE, 'IE���', $COUNT_IE, 0, \@agent_ie);
	undef @agent_ie;
	print "\n\n<BR>\n\n<A name=share_nn></A>\n";
	&Macro_PutTable_a(2, 'NNƱ�ΤΥ�����', 'NN�С������', $COUNT_NN, 'NN���', $COUNT_NN, 0, \@agent_nn);
	undef @agent_nn;
	print "\n\n<BR>\n\n<A name=share_os></A>\n";
	&Macro_PutTable_a(0, '����OS����', 'OS����(����)', $COUNT_OS, '', 0, 0, \@agent_os);
	undef @agent_os;
	print "\n</TD></TR></TABLE></CENTER><BR>\n\n";
}

if (($P{MODE} eq 'screen') || ($P{MODE} eq 'all') || ($P{MODE} eq 'solo_analyze') || ($P{MODE} eq 'solo_all')) {
	print "<!-- ���̾���� -->\n<CENTER><TABLE border=0 cellpadding=8><TR><TD valign=top>\n<A name=screen></A>\n";
	&Macro_PutTable_a(0, '���̾�������', '���̾���', $COUNT_SCREEN, '', 0, 0, \@screen);
	undef @screen;
	print "\n</TD><TD valign=top>\n<A name=screen_size></A>\n";
	&Macro_PutTable_a(0, '������������', '�� x ��', $COUNT_SCREEN_SIZE, '', 0, 0, \@screen_size);
	undef @screen_size;
	print "\n</TD><TD valign=top>\n<A name=screen_color></A>\n";
	&Macro_PutTable_a(0, '������������', '����', $COUNT_SCREEN_COLOR, '', 0, 0, \@screen_color);
	undef @screen_color;
	print "\n</TD></TR></TABLE></CENTER><BR>\n\n";
}


### �׻�����¬�꽪λ
if ($DoPutBenchmark) {
	$CPU_end = (times)[0];
	printf("<DIV align=right>������֡� %.3f CPU��</DIV>\n",$CPU_end-$CPU_start);
}


;#--------------------------------------------------------------------
;#�ޥ���
;#--------------------------------------------------------------------
;### �����Υꥹ�Ȥ���ޥ���
sub Macro_CountRawlog {
	$work{'agent'} = $agent;
	$work{'agent'} =~ s'^!'Mozilla/';
	$work{'agent'} =~ s"\(!(.+)\)"\(compatible; MSIE $1\)";
	$work{'ref'} = $ref;
	$work{'ref'} =~ s'^!'http://';
	$work{'date'} = &func::MakeDate($date);

	if (($DoLink) && ($work{'ref'} =~ /^http/)) {
		$work{'ref'} = &func::MakeLink($work{'ref'}, 2) 
	} else {
		$work{'ref'} = &func::URLdecode($work{'ref'})
	}

	if ($screen eq '-') {
		$work{'screen'} = '-';
	} else {
		split(/,/, $screen);
		$_[0] = &func::C62_Decode($_[0]);
		$_[1] = &func::C62_Decode($_[1]);
		$_[2] = &func::C62_Decode($_[2]);
		$work{'screen'} = "$_[0]x$_[1]x$_[2]";
	}

	$RAWLOG{$filename} .= "[$num] $work{'date'} $host $work{'screen'}\n\t$work{'agent'}\n\t$work{'ref'}\n\n";
	++$COUNT_RAWLOG;
}


;### ���ȸ��򥫥���Ȥ���ޥ���
sub Macro_CountRef {
	# ���������󥸥󤫤�
	if    ($ref =~ '^!\w+\.tinami\.com/')
		{ $flag =  1; ++$REF_SEARCH_SHARE{'TINAMI'}; }

	elsif ($ref =~ '\.surpara\.')
		{ $flag =  2; ++$REF_SEARCH_SHARE{'Surfers Paradice'}; }

	elsif ($ref =~ '^!dir\.yahoo\.')
		{ $flag =  3; ++$REF_SEARCH_SHARE{'Yahoo!(Directory)'}; }

	elsif (($ref =~ '^!\w+\.goo\.ne\.jp/'))
		{ $flag =  4; ++$REF_SEARCH_SHARE{'goo'}; }

	elsif ($ref =~ '^!\w+\.infoseek\.')
		{ $flag =  5; ++$REF_SEARCH_SHARE{'Infoseek'}; }

	elsif ($ref =~ '^!\w+\.msn\.')
		{ $flag =  6; ++$REF_SEARCH_SHARE{'MSN'}; }

	elsif ($ref =~ '^!\w+\.google\.')
		{ $flag =  7; ++$REF_SEARCH_SHARE{'Google'}; }

	elsif ($ref =~ '^!infonavi\.infoweb\.ne\.jp/')
		{ $flag = 8; $REF_SEARCH_SHARE{'InfoNavigator'}; }

	elsif ($ref =~ '^!\w+\.lycos\.')
		{ $flag =  9; ++$REF_SEARCH_SHARE{'Lycos'}; }

	elsif (($ref =~ '^!\w+\.fresheye\.') || ($ref =~ '^!\w+\.jplaza\.'))
		{ $flag = 10; ++$REF_SEARCH_SHARE{'Fresheye'}; }

	elsif ($ref =~ '^!kensaku\.org')
		{ $flag = 11; ++$REF_SEARCH_SHARE{'RingRing'}; }

	elsif ($ref =~ '^!\w+\.excite\.')
		{ $flag = 12; ++$REF_SEARCH_SHARE{'excite'}; }

	elsif ($ref =~ '^!\w+\.altavista\.')
		{ $flag = 13; ++$REF_SEARCH_SHARE{'altavista'}; }

	elsif ($ref =~ '^!search\.odn\.ne\.jp/')
		{ $flag = 14; ++$REF_SEARCH_SHARE{'ODN'}; }

	elsif ($ref =~ '^!\w+\.search\.biglobe\.ne\.jp/')
		{ $flag = 15; ++$REF_SEARCH_SHARE{'Biglobe'}; }

	elsif ($ref =~ '^!search\.yahoo\.')
		{ $flag = 16; ++$REF_SEARCH_SHARE{'Yahoo!(Keyword)'}; }

	elsif ($ref =~ '^!google\.yahoo\.')
		{ $flag = 17; ++$REF_SEARCH_SHARE{'Yahoo!(Google)'}; }


	# �̾��URL
	else {
		$flag = 0;
		$flg = 0;

		# �������Ȥ������å�
		foreach (@MySite) {
			if ($ref =~ /^$_/) {
				$ref =~ s/^$_//;
				$ref = '/' if ($ref eq '');
				++$REF_OWN{"$ref <B>&gt;&gt; $filename</B>"};
				++$REF{'-own-'};
				$flg = 1;
				last;
			}
		}
		++$REF{$ref} if ($flg == 0);
	}

	# ���������󥸥󥭡���ɿ���ʬ��
	if ($flag > 0) {
		++$REF{'-search-'};
		split(/&/, $ref);
		foreach $_ (@_) {
			s/%20|\+|\|/ /gi;								# ����®�٤δط��Ǥ��ʤ�ۣ��
#			s/%81@|%81b|\+|\|/ /gi;								# ����®�٤δط��Ǥ��ʤ�ۣ��

			# TINAMI
			if ($flag == 1) {
				++$REF_TINAMI{$1} if (/(\w\w)=yes/ || /word=(.+)/);
				++$REF_TINAMI{"[Charlotte] $1"} if (/key=(.+)/);
			}

			# Surfers Paradice
			elsif ($flag == 2) {
				++$REF_SP{$1}	if ((/J=(.+)/) || (/search=(.+)/));
			}

			# Yahoo!
			elsif ($flag == 3) {
				++$REF_SEARCH{$1}	if (/p=(.+)/);
				++$REF_SEARCH{"<I>[Yahoo C]</I> $1"}	if (/r=(.+)/);
			}

			# goo
			elsif ($flag == 4) {
				++$REF_SEARCH{$1}	if (/MT=(.+)/ || /AW\w=(.+)/);
			}

			# infoseek
			elsif ($flag == 5) {
				++$REF_SEARCH{$1}	if (/qt=(.+)/ || /oq=(.+)/);
			}

			# MSN, Biglobe
			elsif (($flag == 6) || ($flag == 15)) {
				++$REF_SEARCH{$1}	if (/q=(.+)/ || /aq=(.+)/ || /MT=(.+)/);
			}

			# Google, excite, altavista
			elsif (($flag == 7) || ($flag == 12) || ($flag == 13)) {
				++$REF_SEARCH{$1}	if (/q=(.+)/);
			}

			# infoweb, ODN
			elsif (($flag == 8) || ($flag == 14)) {
				++$REF_SEARCH{$1}	if (/QueryString=(.+)/ || /OLDQUERYDISPLAY=(.+)/);
			}

			# lycos
			elsif ($flag == 9) {
				++$REF_SEARCH{$1}	if (/query=(.+)/);
			}

			# fresheye
			elsif ($flag == 10) {
				++$REF_SEARCH{$1}	if (/kw=(.+)/);
			}

			# RingRing
			elsif ($flag == 11) {
				++$REF_SEARCH{$1}	if (/key=(.+)/);
			}

			# Yahoo! (search, google)
			elsif (($flag == 16) || ($flag == 17)) {
				++$REF_SEARCH{$1}	if (/p=(.+)/);
			}
		}
	}
	# ++$REF{$ref};
}


;### �ۥ���̾�η��������̤�������Ȥ���ޥ���
sub Macro_CountHost {
	split(/\./, $host);

	if (($host eq '') || ($host eq '-')) {						#'-'�����ʤ��ä���
		++$HOST_DM{'-'};
	}

	### FQDN
	elsif ($_[$#_] =~ /[a-z]$/) {
		## ccTLD
		if (length($_[$#_]) == 2) {
			++$HOST_DM{ $_[$#_] };
			$host = "*.$_[$#_-2].$_[$#_-1].$_[$#_]";

			# ���ܤ�ǰ����
			if ($_[$#_] eq 'jp') { ++$HOST_DM_JP{$_[$#_-1]}; }
		}

		## gTLD
		else {
			++$HOST_DM{'us'};
			++$HOST_DM_US{ $_[$#_] };
			$host = "*.$_[$#_-1].$_[$#_]";
		}
	}

	### IP
	else {
		++$HOST_DM{'ipaddr'};
		$host = "$_[$#_-3].$_[$#_-2].$_[$#_-1].*";
	}

	++$HOST{$host};
}


;### �����������̾�����̤�������Ȥ���ޥ���
sub Macro_CountAgent {
	### Mozzila��
	if ($agent =~ /^!/) {
		$agent =~ '^!([\w.-]+)\s';					# NN�Υ᥸�㡼�С�����������
		$nnver = $1;

		$agent =~ /\((.*)\)/;						# ���������̩��Ĵ�٤����
		split(/; /, $1);

		# IE��
		if ($_[0] =~ /^!([\w.-]+)/) {
			# NetCaptor
			if ($_[2] =~ /^NetCaptor/) {
				++$AGENT{'NetCaptor'};			
			}

			# ��IE
			else {
				++$AGENT{'Internet Explorer'};		# IE���ΤΥ�����
				++$AGENT_IE{$1};					# IE�Υ᥸�㡼�С������

				### IE�ξ���OS����
				if    ($_[1] eq 'Windows 98')     { ++$AGENT_OS{'Windows 98'}; }
				elsif ($_[1] eq 'Windows NT 5.0') { ++$AGENT_OS{'Windows 2000'}; }
				elsif ($_[1] eq 'Windows NT 5.1') { ++$AGENT_OS{'Windows XP'}; }
				elsif ($_[1] eq 'Windows NT 6.0') { ++$AGENT_OS{'Windows Vista'}; }
				elsif ($_[1] eq 'Windows 95')     { ++$AGENT_OS{'Windows 95'}; }
				elsif ($_[1] eq 'Windows NT 4.0') { ++$AGENT_OS{'Windows NT'}; }	# ¿ʬ
				elsif ($_[1] eq 'Windows NT')     { ++$AGENT_OS{'Windows NT'}; }
				elsif ($_[1] =~ /^MSN|^AOL/)      { ++$AGENT_OS{$_[2]}; }
				elsif ($_[1] eq 'Mac_PowerPC')    { ++$AGENT_OS{'Macintosh'}; }
				elsif ($_[1] eq 'Win32')          { ++$AGENT_OS{'Windows 95'}; }	# ¿ʬ
				elsif ($_[1] eq 'Windows 3.1')    { ++$AGENT_OS{'Windows 3.1'}; }
				# else { ++$AGENT_OS{'-etc-'}; print "$agent<BR>\n"; }
				#elsif ($_[1] =~ ".*Firefox/")	{++$AGENT{'Firefox'};
			}
		}


		# NN��
		elsif (($_[1] =~ /\bI\b/) || ($_[1] =~ /\bU\b/) || ($_[1] =~ /\bN\b/)) {
			++$AGENT{'Netscape Navigator'};		# NN���ΤΥ�����
			++$AGENT_NN{$nnver};

			### OS����
			if    (($_[0] eq 'Win98') || ($_[2] eq 'Win98'))
				{ ++$AGENT_OS{'Windows 98'}; }
			elsif (($_[0] eq 'Windows NT 5.0') || ($_[2] eq 'Windows NT 5.0'))
				{ ++$AGENT_OS{'Windows 2000'}; }
			elsif (($_[0] eq 'Win95') || ($_[2] eq 'Win95'))
				{ ++$AGENT_OS{'Windows 95'}; }
			elsif (($_[0] eq 'WinNT') || ($_[2] eq 'WinNT'))
				{ ++$AGENT_OS{'Windows NT'}; }
			elsif (($_[0] eq 'WinNT4.0') || ($_[2] eq 'WinNT4.0'))
				{ ++$AGENT_OS{'Windows NT'}; }
			elsif (($_[0] eq 'Macintosh') || ($_[2] eq 'Macintosh'))
				{ ++$AGENT_OS{'Macintosh'}; }
			elsif (($_[0] eq 'Win16') || ($_[2] eq 'Win16'))
				{ ++$AGENT_OS{'Windows 3.1'}; }
			elsif ($_[0] eq 'OS/2')
				{ ++$AGENT_OS{'OS/2'}; }
			# Xü���ξ��Ϥ⤦������ʬ����
			elsif ($_[0] eq 'X11')
				{ $_[2] =~ /^([^\s]+)/; ++$AGENT_OS{$1}; }
			# else { ++$AGENT_OS{'-etc-'}; print "$agent<BR>\n"; }
		}

		# ����¾����ѥ�
		elsif ($_[0] eq 'compatible') {
			if ($_[1] =~ '^([^/]*)/.*') {		# ver.ɽ��������äݤ�
				++$AGENT{$1};					# ver.ɽ������
			} else {
				++$AGENT{$_[1]};				# ���Τޤ޺���
			}
		}

		# ���������櫓�Ǥ�ʤ���̯��Ω��Τ��
		else {
			if ($_[0] =~ "^DreamPassport/") {
				++$AGENT{'DreamPassport'};
			} elsif ($_[0] =~ "^PNWalker/") {
				++$AGENT{'PNWalker'};
			} elsif (($nnver == 3.01) && (!$_[1])) {	# CacheFlow
				++$AGENT{'CacheFlow'};
			} else {					# �����˥ޥ��ʡ���
				++$AGENT{'-etc-'};
			}
		}
	}

	### Mozilla��̾���ʤ���Ω��
	else {
		if ($agent =~ '^([^/]*)/.*') {			# ver.ɽ��������äݤ�
			++$AGENT{$1};						# ver.ɽ������
		} else {
			++$AGENT{$agent};					# ���Τޤ޺���
		}
	}
}


;### ���̾���򥫥���Ȥ���ޥ���
sub Macro_CountScreen {
	unless (($screen eq '') || ($screen eq '-')) {
		split(/,/, $screen);
		$_[0] = &func::C62_Decode($_[0]);
		$_[1] = &func::C62_Decode($_[1]);
		$_[2] = &func::C62_Decode($_[2]);
		++$SCREEN{"$_[0]x$_[1]x$_[2]"};
		++$SCREEN_SIZE{"$_[0]x$_[1]"};
		++$SCREEN_COLOR{"$_[2]"};
	}
}


;### �����ɤ䵭����̣����ʸ������Ѵ�����
sub Macro_ChangeList {
	### ���ȸ�
	foreach (@ref) {
		($n, $data) = split(/\t/);

		if ($data eq '-') {
			$data = '�֥å��ޡ��������������꤫�� / ��ܥåȡ���󥽥ե� / URLľ�Ǥ� / ���ȸ����ä��ƤΥ�������';
		} elsif ($data eq 'noscript') {
			$data = 'JavaScript��ػߡ����ϻ��ѽ���ʤ��֥饦���ˤ�껲�ȸ���������';
		} elsif ($data eq '-own-') {
			$data = '����������Ǥΰ�ư';
		} elsif ($data eq '-search-') {
			$data = '(efStat����Ͽ����Ƥ���)���������󥸥󤫤�';
		} else {
			$data =~ s"^!"http://";
			if (($DoLink) && ($data =~ /^http/)) {
				$data = &func::MakeLink($data, 1);
			} else {
				$data = &func::URLdecode($data);
			}
		}

		$_ = "$n\t$data";
	}

	### ���������ưʬ��
	&change_a(\@ref_own);

	### ���������󥸥�
	&change_a(\@ref_search);

	### TINAMI���ƥ���
	foreach (@ref_tinami) {
		($n, $data) = split(/\t/);

		if ($TABLE{'tinami'}{$data}) {
			$data = "[C] $TABLE{'tinami'}{$data}";
		} else {
			$data = &func::URLdecode($data);
		}

		$_ = "$n\t$data";
	}

	## Surfers Paradice
	&change_a(\@ref_sp);


	### ����ȥ꡼������
	foreach (@host_dm) {
		($n, $data) = split(/\t/);

		if ($data eq 'ipaddr') {
			$data = "�ɥᥤ��Ƚ�̤Ǥ��� (<B>IP���ɥ쥹</B>)";
		} elsif ($data eq '-') {
			$data = "<B><FONT SIZE=+1>[�ٹ�] IP��Ͽ̵��</FONT><BR>(�����󥿤�TELNET����ľ�ܼ¹�?)</B>";
		} elsif ($TABLE{'cctld'}{$data}) {
			$data = "$TABLE{'cctld'}{$data} (\*.<B>${data}<\/B>)";
		} else {
			$data = "̤����ι��ҥ����� (*.<B>${data}<\/B>)";
		}

		$_ = "$n\t$data";
	}

	## ������2��٥�ɥᥤ��
	foreach (@host_dm_jp) {
		($n, $data) = split(/\t/);

		if ($TABLE{'jpdomain'}{$data}) {
			$data = "$TABLE{'jpdomain'}{$data} (\*.<B>${data}<\/B>.jp)";
			$_ = "$n\t$data";
		}
	}

	## �ƹ���2��٥�ɥᥤ��
	foreach (@host_dm_us) {
		($n, $data) = split;

		if ($TABLE{'gtld'}{$data}) {
			$data = "$TABLE{'gtld'}{$data} (\*.<B>${data}<\/B>)";
			$_ = "$n\t$data";
		}
	}

	### User Agent
	foreach (@agent) {
		($n, $data) = split(/\t/);

		if ($data eq '-etc-') {
			$data = "����¾";
		} elsif ($data eq '-') {
			$data = "̾������";
		} elsif ($TABLE{'agent'}{$data}) {
			$data = "${data}<BR>$TABLE{'agent'}{$data}";
		}

		$_ = "$n\t$data";
	}

	foreach (@screen_color) {
		($n, $data) = split;

		$data = "${data}bit";
		$_ = "$n\t$data";
	}

	sub change_a {
		my($array) = @_;
		my($line, $n, $data);
		foreach $line (@$array) {
			($n, $data) = split(/\t/, $line);
			$data = &func::URLdecode($data);
			$line = "$n\t$data";
		}
	}
}


;### �����ѤΥơ��֥����
;### ɽ���⡼��, ɽ��, ����, ����, ������1, ������2(����), ɽ������, ɽ������������
sub Macro_PutTable_a {
	my($mode, $title, $item, $div, $sub1, $sub2, $limit, $array) = @_;
	my($buf, $n, $data, $line, $ave, $width);

	unless (@$array == ()) {
		if (($sub2==0) || ($SAMPLES==0)) { $ave = 0; }							#0�����к�
		else { $ave = sprintf("%2.1f", ($sub2*100)/$SAMPLES); }

		### ɽ��
		print "<TABLE border=1 cellspacing=0 cellpadding=1${tbc[5]}>\n";

		print "\t<TR><TH nowrap colspan=2${tbc[0]}><A HREF=\"#menu\"><FONT size=+1>�� $title ��</FONT></A><BR>";
		if    ($mode == 0) { print "<FONT size=-1>(����ץ���� : $div)</FONT>"; }																				#�̾�ɽ��
		elsif ($mode == 1) { print "(<SUP>$sub1 : $sub2 ($ave%)</SUP> / <SUB>���� : $SAMPLES</SUB>)<BR><FONT size=-1>(ͭ������ץ���� : $div)</FONT>"; }		#TINAMI,SPʬ����
		elsif ($mode == 2) { print "(<SUP>$sub1 : $sub2 ($ave%)</SUP> / <SUB>���� : $SAMPLES</SUB>)"; }															#����ɥᥤ��,IE������,NN��������
		print "</TH></TR>\n";

		### ɽ�ι���
		print "\t<TR><TH nowrap${tbc[1]}>���</TH>";
		print "<TH${tbc[2]}>$item</TH></TR>\n";

		### ɽ�����
		foreach $line (@$array) {
			($n, $data) = split(/\t/, $line);
			$n = int($n);

			if (($n==0) || ($div==0)) { $ave = 0; }
			else {
				$ave_old = $ave;
				$ave = sprintf("%2.1f",($n*100)/$div);
				$width = int($ave);
				$width = 1 if ($width < 1);
			}

			print "\t<TR><TD>";
			print "<IMG src=\"lib/b.gif\" height=10 width=${width}>" if ($DoPutGraph);
			print " $n";
			if ($ave_old != $ave) { print " ($ave%)"; }
			print "</TD>";

			print "<TD${tbc[6]}>${data}</TD></TR>\n";
		}

		### ɽ�����¤����ꤵ��Ƥ����硢����ɽ��
		print "\t<TR><TD colspan=2 align=right${tbc[0]}><FONT size=-1><B>$limit��ʲ���ά</B></FONT></TD></TR>\n" unless ($limit == 0);
		print "</TABLE>\n";
	}
}


;### �����󥿽���ɽ - ���֤�
;### ɽ��������, ���ܼ���, Ϣ������
;### ������: 0=�̾�, 1=[����������]���ʤ�, 2=[��]���ʤ�, 3=ξ��̵��
sub Macro_PutTable_b {
	my($type, $ptr, $hash) = @_;
	my($colspan, @sum);

	if   (($type==2) || ($type==3)) {						#[�ڡ�����]��ɽ�����ʤ�
		$colspan = @$ptr;
	} else { $colspan = @$ptr+1; }

	### ����(ɽ��)
	print "<TABLE border=1 cellspacing=0 cellpadding=1${tbc[6]}>\n";
	print "\t<TR><TH colspan=${colspan}${tbc[0]}><A href=\"#menu\"><FONT size=+1>�� $ptr->[0] ��</FONT></A></TH></TR>\n";

	### �� : ����
	print "\t<TR${tbc[5]}><TH nowrap${tbc[1]}>��</TH>";
	for ($i=1 ; $i < @$ptr ; $i++) { print "<TH>$ptr->[$i]</TH>"; }
	### �� : �ڡ�����
	print "<TH${tbc[4]}>�ڡ�����</TH>" unless (($type==2) || ($type==3));
	print "</TR>\n";

	### �� : ����
	foreach (@filename) {
		print "\t<TR align=right><TH${tbc[2]}>$_</TH>";

		split(/\t/, $$hash{ $_ });
		foreach (@_) {
			$_ = &func::C62_Decode($_);
		}
		$all = &func::CalcSum(@_);

		for ($i=0 ; $i < @$ptr-1 ; $i++) {
			if (($_[$i]==0) || ($all==0)) { $ave = 0; }
			else {
				$ave = sprintf("%2.1f",($_[$i]*100)/$all);
			}
			$height = int($ave);
			$height = 1 if ($height < 1);

			print "<TD valign=\"bottom\">";
			print "<IMG src=\"lib/b.gif\" height=${height} width=10 alt=\"$ave%\"><BR>" if ($DoPutGraph);
			print "$_[$i]";
			print "</TD>";
			$sum[$i] += $_[$i];
		}
		### �� : [�ڡ�����]
		unless (($type==2) || ($type==3)) {
			print "<TH${tbc[8]}>$all</TH>";
		}
		print "</TR>\n";
	}

	### �� : ����������
	unless (($type==1) || ($type==3)) {
		print "\t<TR align=right${tbc[7]}><TH nowrap${tbc[3]}>�����ȷ�</TH>";
		$all = &func::CalcSum(@sum);
		foreach (@sum) {
			if (($_==0) || ($all==0)) { $ave = 0; }
			else {
				$ave = sprintf("%2.1f",($_*100)/$all);
			}
			$height = int($ave);
			$height = 1 if ($height < 1);

			print "<TH valign=\"bottom\">";
			print "<IMG src=\"lib/b.gif\" height=${height} width=10 alt=\"$ave%\"><BR>" if ($DoPutGraph);
			print "$_";
			print "</TH>";
		}
		### �� : ������ ([�ڡ�����] = [�����ȷ�])
		printf("<TH%s>%d</TH>",${tbc[9]}, $all) unless ($type==2);
		print "<TR>\n";
	}

	print "</TABLE>\n";
}


;### �����󥿽���ɽ - ���֤�
;### ɽ��������, ���ܼ���, ɽ��, ñ��, ���ܿ�, Ϣ������
;### ������: 0=�̾�, 1=[����������]���ʤ�, 2=[��]���ʤ�, 3=ξ��̵��
;### ���̥⡼��: 0=�̾�, 1=�����̽���, 2=���̽���
sub Macro_PutTable_c {
	my($type, $mode, $title, $sub, $max, $assoc_array) = @_;
	my($colspan, @sum, @d, @w);
	@w=('��','��','��','��','��','��','��');

	if   (($type==2) || ($type==3)) {						#[�ڡ�����]��ɽ�����ʤ�
		$colspan = $max+1;									# -> ��򸺤餹
	} else { $colspan = $max+2; }

	### ����(ɽ��)
	print "<TABLE border=1 cellspacing=0 cellpadding=1${tbc[6]}>\n";
	print "\t<TR><TH colspan=${colspan}${tbc[0]}><A href=\"#menu\"><FONT size=+1>�� $title ��</FONT></A></TH></TR>\n";

	### �� : ����
	print "\t<TR${tbc[5]}><TH nowrap${tbc[1]}>��</TH>";
	for ($i=0 ; $i < $max ; $i++) {
		print "<TH>";
		if    ($mode == 0) { print "$i$sub"; }				#�̾�
		elsif ($mode == 1) { print "$w[$i]$sub"; }			#�����̽���
		elsif ($mode == 2) { printf("%d$sub", $i+1); }		#���̽���
		print "</TH>";
	}
	### �� : �ڡ�����
	unless (($type==2) || ($type==3)) { print "<TH${tbc[4]}>�ڡ�����</TH>"; }
	print "</TR>\n";

	### �� : ����
	foreach $line (@filename) {
		print "\t<TR align=right><TH${tbc[2]}>$line</TH>";

		split(/\t/, $$assoc_array{ $line });

		for ($i=0 ; $i < $max ; $i++) {
			$_[$i] = &func::C62_Decode($_[$i]);
			print "<TD>$_[$i]</TD>";
			$sum[$i] += $_[$i];
		}
		### �� : [�ڡ�����]
		unless (($type==2) || ($type==3)) {
			printf("<TH%s>%d</TH>",${tbc[8]}, &func::CalcSum(@_));
		}
		print "</TR>\n";
	}

	### �� : ����������
	unless (($type==1) || ($type==3)) {
		print "\t<TR align=right${tbc[7]}><TH nowrap${tbc[3]}>�����ȷ�</TH>";
		for ($i=0 ; $i < $#sum+1 ; $i++) { print "<TH>$sum[$i]</TH>"; }
		### �� : ������ ([�ڡ�����] = [�����ȷ�])
		unless ($type==2) { printf("<TH%s>%d</TH>",${tbc[9]}, &func::CalcSum(@sum)); }
		print "<TR>\n";
	}

	print "</TABLE>\n";
}
1;
