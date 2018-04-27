;#+------------------------------------------------------------------------
;#|efStat
;#|スタートアップルーチン
;#+------------------------------------------------------------------------
;# ※ここからは分かる人だけ弄って下さい。
;# 　(タブのサイズ・[4]、折返し・[無し]で綺麗に表示されます)
;#+------------------------------------------------------------------------
;#|&main
;#+------------------------------------------------------------------------
### [初期設定]
$ENV{'TZ'} = 'JST-9';													# 環境変数TZを日本時間に設定する
$Limit_Analyzer = 100000;												# 解析できるログの行数
$html_title = 'メニュー';												# 初期タイトル
$cookie_id = $self = "http://$ENV{'HTTP_HOST'}$ENV{'SCRIPT_NAME'}";		# 自分自身のURL(クッキーの名前)
$Dir_Log = "./${Dir_Log}/";												# ログディレクトリを修正

# 項目
%koumoku = (
	day		=> ['日別集計',		'本日',   '昨日','一昨日','3日前','4日前','5日前','6日前','一週前'],
	weekly	=> ['週別集計',		'今週',   '先週','2週前','3週前','4週前','一月前'],
	month	=> ['月別集計',		'1月',    '2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月'],
	hour	=> ['時間帯別集計',	'0時',    '1時','2時','3時','4時','5時','6時','7時','8時','9時','10時','11時','12時','13時','14時','15時','16時','17時','18時','19時','20時','21時','22時','23時'],
	week	=> ['曜日別集計',	'日曜日', '月曜日','火曜日','水曜日','木曜日','金曜日','土曜日'],
	year	=> ['年度別集計',	'今年',   '昨年','一昨年','3年前','4年前','5年前'],
);

### 各ライブラリのありか
$lib_jcode      = './lib/jcode.pl';
$lib_fstat_func = './lib/func.pl';
$lib_fstat_main = './lib/main.pl';
$lib_fstat_menu = './lib/menu.pl';


### 表に色が指定されている場合、色指定タグの前にスペースを追加
for ($i=0 ; $i <= $#tbc ; $i++ ) { $tbc[$i] = " $tbc[$i]" if ($tbc[$i] ne ''); }

### 共用関数の読み込み
unless (-e $lib_fstat_func) {
	print "Content-type: text/html\n\n<HTML>\n";
	print "<HEAD><META http-equiv=\"Content-Type\" content=\"text/html; charset=EUC-JP\"><TITLE>efStat $ver / 異常終了</TITLE></HEAD>\n";
	print "<BODY><P>efStat用関数ファイル ($lib_fstat_func) が見つかりませんでした。<BR>処理を続行できません。</P></BODY>\n";
	print "</HTML>\n";
	exit(1);
}
require $lib_fstat_func;


### jcode.plを読み込む
unless (-e $lib_jcode) {
	&func::PutError("jcode.pl を読み込むことができませんでした。<BR>位置の指定に誤りがないか確認下さい。");
}
require $lib_jcode;

### 予め、efStatが解釈できる形に変換しておく
foreach (@MySite) {
	$_ =~ s'http://'!';
}

foreach (@Complete_URL) {
	$$_[0] =~ s'^http://'!';
	&jcode::convert(\$$_[1], 'euc', '', 'z');
}


### main読み込み準備
unless (-e $lib_fstat_main) { &func::PutError("ログ解析ルーチン ($lib_fstat_main) が見つかりませんでした。<BR>処理を続行できません。"); }

### menu読み込み準備
unless (-e $lib_fstat_menu) { &func::PutError("メニューファイル ($lib_fstat_menu) が見つかりませんでした。<BR>処理を続行できません。"); }

### クッキーを受け取る
&Get_Cookie;

### オプションの状態を変更する
&radiobtn;

### 標準入力やクエリから引数を取得
&Get_Strings;


### [処理を分岐]

### メニュー画面
if (($ENV{'CONTENT_LENGTH'} == 0) && ($ENV{'QUERY_STRING'} eq '')) {
	&html_head;
	require $lib_fstat_menu;
	&html_tail;
	exit(0);
}
### ログ複数表示モード
elsif ($ENV{'REQUEST_METHOD'} eq 'POST') {
	# &func::PutError("外部から実行不可。<BR>メニューを外のサイトに置いていたりしませんか？") if ($self ne $ENV{'HTTP_REFERER'});

	### ファイル一覧を取得
	opendir(DIR, "$Dir_Log");
	unless (-e $Dir_Log) { closedir(DIR); &func::PutError("指定されたログディレクトリ ($Dir_Log) は存在しません。<BR>指定に誤りがないか確認下さい。"); }
	unless (-r $Dir_Log) { closedir(DIR); &func::PutError("ログディレクトリが読み出し禁止属性になっています。<BR>ファイル一覧を取得できません。<BR>パーミッションを確認して下さい(705又は755にして下さい)。"); }
	@filename = grep(s/\.[lL][oO][gG]$//, readdir(DIR));
	@filename = sort({$a cmp $b} @filename);

	### 入力内容を内部変数にコピー
	&copy2list;

	### 入力された変数をチェック
	if (($DoTasteless > 1) || ($DoPutGraph > 1) ||
	    ($DoLink > 1) || ($DoSaveCookie > 1)
	) { &func::PutError('仕様に無いオプション指定です。'); }
	elsif (($Limit_Log > 999)    || ($Limit_Ref > 999)    || ($Limit_Tinami > 999) ||
	       ($Limit_Sp > 999)     || ($Limit_Search > 999) || ($Limit_Host > 999)   ||
	       ($Limit_Domain > 999) || ($Limit_Jp > 999)     || ($Limit_Agent > 999)
	) { &func::PutError('仕様に無い制限指定です。'); }

	### クッキーの保存が許可されているならクッキーを保存しておく
	if ($DoSaveCookie) {
		&copy2cookie;
		&Set_Cookie;
	}

	### タイトル設定
	$html_title = 'ログ一括表示';
	if    ($P{MODE} eq 'rawlog') { $html_title .= ' / 生ログ'; }
	elsif ($P{MODE} eq 'count')  { $html_title .= ' / カウント数集計'; }
	elsif ($P{MODE} eq 'all')    { $html_title .= ' / 全て'; }
	elsif ($P{MODE} eq 'ref')    { $html_title .= ' / 参照元統計(系)'; }
	elsif ($P{MODE} eq 'host')   { $html_title .= ' / ホスト統計(系)'; }
	elsif ($P{MODE} eq 'ua')     { $html_title .= ' / ブラウザ統計(系)'; }
	elsif ($P{MODE} eq 'screen') { $html_title .= ' / 画面情報統計(系)'; }
	else                         { &func::PutError('仕様に無いモード指定です。'); }

	if    ($P{d} eq 't')         { $html_title .= " / 本日分のみ"; }
	elsif ($P{d} eq 'y')         { $html_title .= " / 昨日分のみ"; }
}
### ログ単体表示モード(Webstat互換)
elsif ($ENV{'REQUEST_METHOD'} eq 'GET') {
	$filename[0]	= (split(/&/,$alldata))[0];

	$html_title = 'ログ単体表示';
	if    ($P{'m'} eq '0') { $P{MODE} = 'solo_rawlog';  $html_title .= " / $filename[0] (生ログのみ)"; }
	elsif ($P{'m'} eq '1') { $P{MODE} = 'solo_analyze'; $html_title .= " / $filename[0] (解析結果のみ)"; }
	else                   { $P{MODE} = 'solo_all';     $html_title .= " / $filename[0] (全て表\示)"; }

	if    ($P{d} eq 't')   { $html_title .= ' / 本日分のみ'; }
	elsif ($P{d} eq 'y')   { $html_title .= ' / 昨日分のみ'; }
}


### 表の色を取り去る
if ($DoTasteless) {
	$html_body  = '<BODY bgcolor=#ffffff text=#000000 link=#7726c8 alink=#5c4fff vlink=#ff5959>';
	foreach (@tbc) { $_ = ''; }
}


### 解析開始
&html_head;
require $lib_fstat_main;
&html_tail;


exit(0);


;#+------------------------------------------------------------------------
;#|マクロ
;#+------------------------------------------------------------------------
### 標準入力やクエリから引数を取得
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


### クッキーを取得
sub Get_Cookie {
	foreach $pair (split(/; / , $ENV{'HTTP_COOKIE'})) {
		($key , $val) = split(/=/ , $pair);
		$all_cookies{$key} = $val;
	}
	if ($all_cookies{$cookie_id} eq '') {	# クッキーがないなら初期化
		&Init_Cookie;
	} else {								# クッキーがあるなら読み込み
		foreach $pair (split(/&/, $all_cookies{$cookie_id})) {
			($key , $val) = split(/:/ , $pair);
			$key = &func::URLdecode($key);
			$val = &func::URLdecode($val);
			$COOKIE{$key} = $val;
		}
	}
}


### クッキーを設定
sub Set_Cookie {
	@pairs = ();

	foreach $key (sort(keys(%COOKIE))) {
		$val = $COOKIE{$key};
		push(@pairs , &func::URLencode($key).":".&func::URLencode($val));
	}

	$new_cookie = join('&' , @pairs);
	$date = &func::GmtDate(time + 31536000);		# 1年間保存
	if ($new_cookie ne $all_cookies{$cookie_id}) {
		print "Set-Cookie: $cookie_id=$new_cookie; expires=$date\n";
	}
}


### 入力内容を内部変数にコピー
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


### ユーザから入力された引数をクッキーに渡す
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


### 初めてクッキーの保存をするとき、あらかじめ初期値をセットする
sub Init_Cookie {
	$COOKIE{'OPT_tl'} = 0;	# テイストレス		…NO
	$COOKIE{'OPT_gr'} = 1;	# グラフ表示		…YES
	$COOKIE{'OPT_lk'} = 1;	# リンクを貼るか	…YES
	$COOKIE{'PASS'}   = '';	# パスワード文字列	…空

	$COOKIE{'LM_raw'} = 50;	# 生ログ表示件数	…50件
	$COOKIE{'LM_ref'} = 0;	# 参照元表示下限	…0
	$COOKIE{'LM_tnm'} = 0;	# TINAMI表示下限	…0
	$COOKIE{'LM_sp'}  = 0;	# SP表示下限		…0
	$COOKIE{'LM_key'} = 0;	# キーワード表示下限…0
	$COOKIE{'LM_hst'} = 0;	# ホスト表示下限	…0
	$COOKIE{'LM_dm'}  = 0;	# 国籍表示下限		…0
	$COOKIE{'LM_ua'}  = 0;	# ブラウザ表示下限	…0
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
