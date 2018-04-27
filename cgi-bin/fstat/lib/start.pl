;#+------------------------------------------------------------------------
;#|efStat
;#|�������ȥ��åץ롼����
;#+------------------------------------------------------------------------
;# �����������ʬ����ͤ���Ϯ�äƲ�������
;# ��(���֤Υ�������[4]�����֤���[̵��]������ɽ������ޤ�)
;#+------------------------------------------------------------------------
;#|&main
;#+------------------------------------------------------------------------
### [�������]
$ENV{'TZ'} = 'JST-9';													# �Ķ��ѿ�TZ�����ܻ��֤����ꤹ��
$Limit_Analyzer = 100000;												# ���ϤǤ�����ιԿ�
$html_title = '��˥塼';												# ��������ȥ�
$cookie_id = $self = "http://$ENV{'HTTP_HOST'}$ENV{'SCRIPT_NAME'}";		# ��ʬ���Ȥ�URL(���å�����̾��)
$Dir_Log = "./${Dir_Log}/";												# ���ǥ��쥯�ȥ����

# ����
%koumoku = (
	day		=> ['���̽���',		'����',   '����','�����','3����','4����','5����','6����','�콵��'],
	weekly	=> ['���̽���',		'����',   '�轵','2����','3����','4����','�����'],
	month	=> ['���̽���',		'1��',    '2��','3��','4��','5��','6��','7��','8��','9��','10��','11��','12��'],
	hour	=> ['�������̽���',	'0��',    '1��','2��','3��','4��','5��','6��','7��','8��','9��','10��','11��','12��','13��','14��','15��','16��','17��','18��','19��','20��','21��','22��','23��'],
	week	=> ['�����̽���',	'������', '������','������','������','������','������','������'],
	year	=> ['ǯ���̽���',	'��ǯ',   '��ǯ','���ǯ','3ǯ��','4ǯ��','5ǯ��'],
);

### �ƥ饤�֥��Τ��꤫
$lib_jcode      = './lib/jcode.pl';
$lib_fstat_func = './lib/func.pl';
$lib_fstat_main = './lib/main.pl';
$lib_fstat_menu = './lib/menu.pl';


### ɽ�˿������ꤵ��Ƥ����硢�����꥿�������˥��ڡ������ɲ�
for ($i=0 ; $i <= $#tbc ; $i++ ) { $tbc[$i] = " $tbc[$i]" if ($tbc[$i] ne ''); }

### ���Ѵؿ����ɤ߹���
unless (-e $lib_fstat_func) {
	print "Content-type: text/html\n\n<HTML>\n";
	print "<HEAD><META http-equiv=\"Content-Type\" content=\"text/html; charset=EUC-JP\"><TITLE>efStat $ver / �۾ｪλ</TITLE></HEAD>\n";
	print "<BODY><P>efStat�Ѵؿ��ե����� ($lib_fstat_func) �����Ĥ���ޤ���Ǥ�����<BR>������³�ԤǤ��ޤ���</P></BODY>\n";
	print "</HTML>\n";
	exit(1);
}
require $lib_fstat_func;


### jcode.pl���ɤ߹���
unless (-e $lib_jcode) {
	&func::PutError("jcode.pl ���ɤ߹��ळ�Ȥ��Ǥ��ޤ���Ǥ�����<BR>���֤λ���˸�꤬�ʤ�����ǧ��������");
}
require $lib_jcode;

### ͽ�ᡢefStat�����Ǥ�������Ѵ����Ƥ���
foreach (@MySite) {
	$_ =~ s'http://'!';
}

foreach (@Complete_URL) {
	$$_[0] =~ s'^http://'!';
	&jcode::convert(\$$_[1], 'euc', '', 'z');
}


### main�ɤ߹��߽���
unless (-e $lib_fstat_main) { &func::PutError("�����ϥ롼���� ($lib_fstat_main) �����Ĥ���ޤ���Ǥ�����<BR>������³�ԤǤ��ޤ���"); }

### menu�ɤ߹��߽���
unless (-e $lib_fstat_menu) { &func::PutError("��˥塼�ե����� ($lib_fstat_menu) �����Ĥ���ޤ���Ǥ�����<BR>������³�ԤǤ��ޤ���"); }

### ���å�����������
&Get_Cookie;

### ���ץ����ξ��֤��ѹ�����
&radiobtn;

### ɸ�����Ϥ䥯���꤫����������
&Get_Strings;


### [������ʬ��]

### ��˥塼����
if (($ENV{'CONTENT_LENGTH'} == 0) && ($ENV{'QUERY_STRING'} eq '')) {
	&html_head;
	require $lib_fstat_menu;
	&html_tail;
	exit(0);
}
### ��ʣ��ɽ���⡼��
elsif ($ENV{'REQUEST_METHOD'} eq 'POST') {
	# &func::PutError("��������¹��Բġ�<BR>��˥塼�򳰤Υ����Ȥ��֤��Ƥ����ꤷ�ޤ��󤫡�") if ($self ne $ENV{'HTTP_REFERER'});

	### �ե�������������
	opendir(DIR, "$Dir_Log");
	unless (-e $Dir_Log) { closedir(DIR); &func::PutError("���ꤵ�줿���ǥ��쥯�ȥ� ($Dir_Log) ��¸�ߤ��ޤ���<BR>����˸�꤬�ʤ�����ǧ��������"); }
	unless (-r $Dir_Log) { closedir(DIR); &func::PutError("���ǥ��쥯�ȥ꤬�ɤ߽Ф��ػ�°���ˤʤäƤ��ޤ���<BR>�ե��������������Ǥ��ޤ���<BR>�ѡ��ߥå������ǧ���Ʋ�����(705����755�ˤ��Ʋ�����)��"); }
	@filename = grep(s/\.[lL][oO][gG]$//, readdir(DIR));
	@filename = sort({$a cmp $b} @filename);

	### �������Ƥ������ѿ��˥��ԡ�
	&copy2list;

	### ���Ϥ��줿�ѿ�������å�
	if (($DoTasteless > 1) || ($DoPutGraph > 1) ||
	    ($DoLink > 1) || ($DoSaveCookie > 1)
	) { &func::PutError('���ͤ�̵�����ץ�������Ǥ���'); }
	elsif (($Limit_Log > 999)    || ($Limit_Ref > 999)    || ($Limit_Tinami > 999) ||
	       ($Limit_Sp > 999)     || ($Limit_Search > 999) || ($Limit_Host > 999)   ||
	       ($Limit_Domain > 999) || ($Limit_Jp > 999)     || ($Limit_Agent > 999)
	) { &func::PutError('���ͤ�̵�����»���Ǥ���'); }

	### ���å�������¸�����Ĥ���Ƥ���ʤ饯�å�������¸���Ƥ���
	if ($DoSaveCookie) {
		&copy2cookie;
		&Set_Cookie;
	}

	### �����ȥ�����
	$html_title = '�����ɽ��';
	if    ($P{MODE} eq 'rawlog') { $html_title .= ' / ����'; }
	elsif ($P{MODE} eq 'count')  { $html_title .= ' / ������ȿ�����'; }
	elsif ($P{MODE} eq 'all')    { $html_title .= ' / ����'; }
	elsif ($P{MODE} eq 'ref')    { $html_title .= ' / ���ȸ�����(��)'; }
	elsif ($P{MODE} eq 'host')   { $html_title .= ' / �ۥ�������(��)'; }
	elsif ($P{MODE} eq 'ua')     { $html_title .= ' / �֥饦������(��)'; }
	elsif ($P{MODE} eq 'screen') { $html_title .= ' / ���̾�������(��)'; }
	else                         { &func::PutError('���ͤ�̵���⡼�ɻ���Ǥ���'); }

	if    ($P{d} eq 't')         { $html_title .= " / ����ʬ�Τ�"; }
	elsif ($P{d} eq 'y')         { $html_title .= " / ����ʬ�Τ�"; }
}
### ��ñ��ɽ���⡼��(Webstat�ߴ�)
elsif ($ENV{'REQUEST_METHOD'} eq 'GET') {
	$filename[0]	= (split(/&/,$alldata))[0];

	$html_title = '��ñ��ɽ��';
	if    ($P{'m'} eq '0') { $P{MODE} = 'solo_rawlog';  $html_title .= " / $filename[0] (�����Τ�)"; }
	elsif ($P{'m'} eq '1') { $P{MODE} = 'solo_analyze'; $html_title .= " / $filename[0] (���Ϸ�̤Τ�)"; }
	else                   { $P{MODE} = 'solo_all';     $html_title .= " / $filename[0] (����ɽ\��)"; }

	if    ($P{d} eq 't')   { $html_title .= ' / ����ʬ�Τ�'; }
	elsif ($P{d} eq 'y')   { $html_title .= ' / ����ʬ�Τ�'; }
}


### ɽ�ο�������
if ($DoTasteless) {
	$html_body  = '<BODY bgcolor=#ffffff text=#000000 link=#7726c8 alink=#5c4fff vlink=#ff5959>';
	foreach (@tbc) { $_ = ''; }
}


### ���ϳ���
&html_head;
require $lib_fstat_main;
&html_tail;


exit(0);


;#+------------------------------------------------------------------------
;#|�ޥ���
;#+------------------------------------------------------------------------
### ɸ�����Ϥ䥯���꤫����������
sub Get_Strings {
	if ($ENV{'CONTENT_LENGTH'} > 0) {
		read(STDIN , $alldata , $ENV{'CONTENT_LENGTH'});
	} elsif ($ENV{"QUERY_STRING"} ne '') {
		$alldata = $ENV{'QUERY_STRING'};
	}

	foreach $data (split(/&/,$alldata)) {
		($key , $val) = split(/=/,$data);
		$val = &func::URLdecode($val);
		$P{$key} = $val;
	}
}


### ���å��������
sub Get_Cookie {
	foreach $pair (split(/; / , $ENV{'HTTP_COOKIE'})) {
		($key , $val) = split(/=/ , $pair);
		$all_cookies{$key} = $val;
	}
	if ($all_cookies{$cookie_id} eq '') {	# ���å������ʤ��ʤ�����
		&Init_Cookie;
	} else {								# ���å���������ʤ��ɤ߹���
		foreach $pair (split(/&/, $all_cookies{$cookie_id})) {
			($key , $val) = split(/:/ , $pair);
			$key = &func::URLdecode($key);
			$val = &func::URLdecode($val);
			$COOKIE{$key} = $val;
		}
	}
}


### ���å���������
sub Set_Cookie {
	@pairs = ();

	foreach $key (sort(keys(%COOKIE))) {
		$val = $COOKIE{$key};
		push(@pairs , &func::URLencode($key).":".&func::URLencode($val));
	}

	$new_cookie = join('&' , @pairs);
	$date = &func::GmtDate(time + 31536000);		# 1ǯ����¸
	if ($new_cookie ne $all_cookies{$cookie_id}) {
		print "Set-Cookie: $cookie_id=$new_cookie; expires=$date\n";
	}
}


### �������Ƥ������ѿ��˥��ԡ�
sub copy2list {
	$DoTasteless  = $P{'OPT_tl'};
	$DoPutGraph   = $P{'OPT_gr'};
	$DoLink       = $P{'OPT_lk'};
	$DoSaveCookie = $P{'OPT_ck'};

	$Limit_Log    = $P{'LM_raw'};
	$Limit_Ref    = $P{'LM_ref'};
	$Limit_Tinami = $P{'LM_tnm'};
	$Limit_Sp     = $P{'LM_sp'};
	$Limit_Search = $P{'LM_key'};
	$Limit_Host   = $P{'LM_hst'};
	$Limit_Domain = $P{'LM_dm'};
	$Limit_Agent  = $P{'LM_ua'};
}


### �桼���������Ϥ��줿�����򥯥å������Ϥ�
sub copy2cookie {
	$COOKIE{'OPT_tl'} = $P{'OPT_tl'};
	$COOKIE{'OPT_gr'} = $P{'OPT_gr'};
	$COOKIE{'OPT_lk'} = $P{'OPT_lk'};
	$COOKIE{'PASS'}   = $P{'PASS'};

	$COOKIE{'LM_raw'} = $P{'LM_raw'};
	$COOKIE{'LM_ref'} = $P{'LM_ref'};
	$COOKIE{'LM_tnm'} = $P{'LM_tnm'};
	$COOKIE{'LM_sp'}  = $P{'LM_sp'};
	$COOKIE{'LM_key'} = $P{'LM_key'};
	$COOKIE{'LM_hst'} = $P{'LM_hst'};
	$COOKIE{'LM_dm'}  = $P{'LM_dm'};
	$COOKIE{'LM_ua'}  = $P{'LM_ua'};
}


### ���ƥ��å�������¸�򤹤�Ȥ������餫�������ͤ򥻥åȤ���
sub Init_Cookie {
	$COOKIE{'OPT_tl'} = 0;	# �ƥ����ȥ쥹		��NO
	$COOKIE{'OPT_gr'} = 1;	# �����ɽ��		��YES
	$COOKIE{'OPT_lk'} = 1;	# ��󥯤�Ž�뤫	��YES
	$COOKIE{'PASS'}   = '';	# �ѥ����ʸ����	�Ķ�

	$COOKIE{'LM_raw'} = 50;	# ����ɽ�����	��50��
	$COOKIE{'LM_ref'} = 0;	# ���ȸ�ɽ������	��0
	$COOKIE{'LM_tnm'} = 0;	# TINAMIɽ������	��0
	$COOKIE{'LM_sp'}  = 0;	# SPɽ������		��0
	$COOKIE{'LM_key'} = 0;	# �������ɽ�����¡�0
	$COOKIE{'LM_hst'} = 0;	# �ۥ���ɽ������	��0
	$COOKIE{'LM_dm'}  = 0;	# ����ɽ������		��0
	$COOKIE{'LM_ua'}  = 0;	# �֥饦��ɽ������	��0
}


sub radiobtn {
	if ($COOKIE{'OPT_tl'}) {
		$check_tl0 = ' checked';
		$check_tl1 = '';
	} else {
		$check_tl0 = '';
		$check_tl1 = ' checked';
	}

	if ($COOKIE{'OPT_gr'}) {
		$check_gr0 = ' checked';
		$check_gr1 = '';
	} else {
		$check_gr0 = '';
		$check_gr1 = ' checked';
	}

	if ($COOKIE{'OPT_lk'}) {
		$check_lk0 = ' checked';
		$check_lk1 = '';
	} else {
		$check_lk0 = '';
		$check_lk1 = ' checked';
	}

	if ($COOKIE{'OPT_ck'}) {
		$check_ck0 = ' checked';
		$check_ck1 = '';
	} else {
		$check_ck0 = '';
		$check_ck1 = ' checked';
	}
}
