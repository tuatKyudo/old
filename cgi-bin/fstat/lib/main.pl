;#+------------------------------------------------------------------------
;#|efStat
;#|ログ解析ルーチン
;#+------------------------------------------------------------------------

if (($P{PASS} ne $Pass) && ($DoPass)) {
	print "<CENTER><P><B>[エラー]</B>パスワードが一致しませんでした。</P></CENTER>\n";
	&html_tail;
	exit(1);
}


;### 計算時間測定開始
$CPU_start = (times)[0] if ($DoPutBenchmark);

### コード変換用テーブルを読み込む
$TABLE{'agent'}    = &func::LoadTable('./lib/table/agent.tbl');
$TABLE{'cctld'}    = &func::LoadTable('./lib/table/cctld.tbl');
$TABLE{'gtld'}     = &func::LoadTable('./lib/table/gtld.tbl');
$TABLE{'jpdomain'} = &func::LoadTable('./lib/table/jpdomain.tbl');
$TABLE{'tinami'}   = &func::LoadTable('./lib/table/tinami.tbl');

foreach $filename (@filename) {
	if ($filename eq '') { next; }		# ".log"ファイル対策
	
	### ファイルをオープン
	unless (open(LOG,"<${Dir_Log}${filename}.log")) {
		print "<CENTER><P><B>[エラー]</B>アクセスログ ( ${Dir_Log}${filename}.log ) を開くことができません。<BR>そのファイルは本当に存在しているか、パーミッションは正しいか (606又は666) などを確認下さい。</P></CENTER>\n";
		&html_tail;
		exit(1);
	}
	flock(LOG,2);

	### プログラム実行時刻を取得
	($SEC,$MIN,$HOUR,$DAY,$MON,$YEAR,$YOUBI,$TOTAL) = localtime(time);

	### ヘッダ部を読み込む＆チェック
	chop($HEAD = <LOG>);
	($LOG_ID, $LOG_SINCE{$filename}) = split(/\t/, $HEAD);
	$LOG_SINCE{$filename} = &func::C62_Decode($LOG_SINCE{$filename});

	if ($LOG_ID ne 'FC2') { next; }

	### 各種情報
	chomp($INFO{$filename} = <LOG>);
	$RANK_ALL{$filename} = &func::C62_Decode((split(/\t/, $INFO{$filename}))[1]);

	### 日別集計
	chomp($DAY{$filename} = <LOG>);
	$RANK_DAY{$filename} = &func::C62_Decode((split(/\t/, $DAY{$filename}))[0]);

	### 時間別集計
	chomp($HOUR{$filename} = <LOG>);

	### 曜日別集計
	chomp($WEEK{$filename} = <LOG>);

	### 週別集計
	chomp($WEEKLY{$filename} = <LOG>);
	$RANK_WEEKLY{$filename} = &func::C62_Decode((split(/\t/, $WEEKLY{$filename}))[0]);

	### 月別集計
	chomp($MONTH{$filename} = <LOG>);
	$RANK_MONTH{$filename} = &func::C62_Decode((split(/\t/, $MONTH{$filename}))[$MON]);

	### 年度別集計
	chomp($YEAR{$filename} = <LOG>);
	# $RANK_YEAR{$filename} = &func::C62_Decode((split(/\t/, $YEAR{$filename}))[0]);

	### アクセスログ集計
	# 解析範囲が指定されている場合
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

	# 全て表示
	else {
		while (chop($LINE = <LOG>)) {
			&Macro_Split;
			&Macro_ProcessLine;
		}
	}

	flock(LOG,8);
	close(LOG);

	### 生ログ用カウンタを初期化しておく
	$COUNT_RAWLOG = 0;

	### 暴走防止用リミッタ
	if ($SAMPLES == $Limit_Analyzer) {
		print "<CENTER><P><B>[エラー]</B>保護機能\が働き、プログラムを強制終了しました。<BR>$Limit_Analyzer件までのログしか処理できないようになっています。<BR>又は、プログラムが暴\走しました。深刻な問題ですので、ぜひ作者にご連絡下さい。</P></CENTER>\n";
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
	&jcode::tr(\$ref, '０-９Ａ-Ｚａ-ｚ　', '0-9a-za-z ');
	$ref = &func::URLencode($ref);
}

sub Macro_ProcessLine {
	### 一番新しいログの記録日時
	$now = $date if ($SAMPLES == 0);

	### 生ログを取得
	if (($P{MODE} eq 'rawlog') || ($P{MODE} eq 'all') || ($P{MODE} eq 'solo_rawlog') || ($P{MODE} eq 'solo_all')) {
		&Macro_CountRawlog() if ($COUNT_RAWLOG < $Limit_Log);
	}

	### 参照元統計, TINAMIカテゴリ分析, Surfers Paradice分析
	&Macro_CountRef() if (($P{MODE} eq 'ref') || ($P{MODE} eq 'all') || ($P{MODE} eq 'solo_analyze') || ($P{MODE} eq 'solo_all'));

	### ホスト名統計, 国籍分析, 国内ドメイン分析
	&Macro_CountHost() if (($P{MODE} eq 'host') || ($P{MODE} eq 'all') || ($P{MODE} eq 'solo_analyze') || ($P{MODE} eq 'solo_all'));

	### ブラウザ統計, ブラウザ分析, スクリーン情報
	&Macro_CountAgent() if (($P{MODE} eq 'ua') || ($P{MODE} eq 'all') || ($P{MODE} eq 'solo_analyze') || ($P{MODE} eq 'solo_all'));

	### スクリーン情報
	&Macro_CountScreen() if (($P{MODE} eq 'screen') || ($P{MODE} eq 'all') || ($P{MODE} eq 'solo_analyze') || ($P{MODE} eq 'solo_all'));

	### サンプリングしたアクセスログの総数
	$SAMPLES++;

	### 一番古いログの記録日時
	$old = $date;
}


### 集計結果をソート
### 連想配列を削除する前に必要な情報を待避しておく
### 不要になった連想配列を削除する
if (($P{MODE} eq 'count') || ($P{MODE} eq 'all')) {
	#総合ランキング
	@rank_all			= &func::MakeList(\%RANK_ALL, \0);
	$COUNT_ALL			= &func::CalcSum(values(%RANK_ALL));
	undef %RANK_ALL;

	#月間ランキング
	@rank_month			= &func::MakeList(\%RANK_MONTH, \0);
	$COUNT_MONTH		= &func::CalcSum(values(%RANK_MONTH));
	undef %RANK_MONTH;

	#週間ランキング
	@rank_weekly		= &func::MakeList(\%RANK_WEEKLY, \0);
	$COUNT_WEEKLY		= &func::CalcSum(values(%RANK_WEEKLY));
	undef %RANK_WEEKLY;

	#本日ランキング
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
	$COUNT_REF			= &func::CalcSum(values(%REF));					#自サイト内参照数
	undef %REF;

	@ref_own			= &func::MakeList(\%REF_OWN, \0);
	$COUNT_OWN			= &func::CalcSum(values(%REF_OWN));				#自サイト内参照数
	undef %REF_OWN;

	@ref_search			= &func::MakeList(\%REF_SEARCH, \$Limit_Search);
	$COUNT_SEARCH		= &func::CalcSum(values(%REF_SEARCH));			#サーチエンジンのキーワード総数
	undef %REF_SEARCH;

	#サーチエンジンから来た数
	@ref_search_share	= &func::MakeList(\%REF_SEARCH_SHARE, \0);
	$COUNT_SEARCH_SHARE	= &func::CalcSum(values(%REF_SEARCH_SHARE));	
	$COUNT_TN_			= $REF_SEARCH_SHARE{'TINAMI'};					#TINAMIから来た数
	$COUNT_SP_			= $REF_SEARCH_SHARE{'Surfers Paradice'};		#SPから来た数
	undef %REF_SEARCH_SHARE;

	@ref_tinami			= &func::MakeList(\%REF_TINAMI, \$Limit_Tinami);
	$COUNT_TN			= &func::CalcSum(values(%REF_TINAMI));			#TINAMIのキーワード総数
	undef %REF_TINAMI;

	@ref_sp				= &func::MakeList(\%REF_SP, \$Limit_Sp);
	$COUNT_SP			= &func::CalcSum(values(%REF_SP));				#SPのキーワード総数
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
	$COUNT_IE			= &func::CalcSum(values(%AGENT_IE));			#IEのシェア
	undef %AGENT_IE;

	@agent_nn			= &func::MakeList(\%AGENT_NN, \0);
	$COUNT_NN			= &func::CalcSum(values(%AGENT_NN));			#NNのシェア
	undef %AGENT_NN;

	@agent_os			= &func::MakeList(\%AGENT_OS, \0);
	$COUNT_OS			= &func::CalcSum(values(%AGENT_OS));			#OSのシェア
	undef %AGENT_OS;
}


if (($P{MODE} eq 'screen') || ($P{MODE} eq 'all') || ($P{MODE} eq 'solo_analyze') || ($P{MODE} eq 'solo_all')) {
	@screen				= &func::MakeList(\%SCREEN, \0);
	$COUNT_SCREEN		= &func::CalcSum(values(%SCREEN));				#有意な画面情報カウント数
	undef %SCREEN;

	@screen_size		= &func::MakeList(\%SCREEN_SIZE, \0);
	$COUNT_SCREEN_SIZE	= &func::CalcSum(values(%SCREEN_SIZE));			#有意な画面情報カウント数
	undef %SCREEN_SIZE;

	@screen_color		= &func::MakeList(\%SCREEN_COLOR, \0);
	$COUNT_SCREEN_COLOR	= &func::CalcSum(values(%SCREEN_COLOR));		#有意な画面情報カウント数
	undef %SCREEN_COLOR;
}



### コードや記号を意味ある文字列に変換する
&Macro_ChangeList;


### 各種情報
if (($P{MODE} eq 'solo_rawlog') || ($P{MODE} eq 'solo_analyze') || ($P{MODE} eq 'solo_all')) {
	$days = ($now-$old)/86400;						#ログを取った期間(日数)
	$now = &func::MakeDate($now);
	$old = &func::MakeDate($old);

	print "<CENTER><TABLE BORDER=2 CELLSPACING=0 CELLPADDING=2>\n";
	print "\t<TR><TH COLSPAN=4${tbc[0]}>対象ログファイル : ${filename[0]}.log</TH></TR>\n";
	print "\t<TR><TH${tbc[1]}>調査期間</TH><TD${tbc[5]}>$old 〜 $now</TD><TH${tbc[2]}>総ヒット数</TH><TD${tbc[6]}>$RANK_ALL{ $filename[0] }</TD></TR>\n";

	if ($days > 0) {
		$ave  = sprintf("%0.2f", $SAMPLES/$days);
		$days = sprintf("%0.2f", $days);
		print "\t<TR><TH COLSPAN=4${tbc[8]}>$SAMPLESアクセス達成に$days日要します　(1日平均 $ave アクセス)</TH></TR>\n";
	}
	print "</TABLE></CENTER><HR>\n\n";
}


### 小メニュー
unless ($P{MODE} eq 'solo_rawlog') {
	### メニュー
	$colspan = 6;		# 列の数
	print "<!-- 小メニュー -->\n<A name=menu></A>\n<CENTER><TABLE border=1 cellspacing=0 cellpadding=1${tbc[0]}>\n\t<TR><TH colspan=${colspan}><FONT size=+1>● 小メニュー ●</FONT></TH></TR>\n";

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
		print "\t<TR><TH colspan=${colspan}${tbc[0]}>■生ログ■</TH></TR>\n";
		&menu_rawlog;
		print "\t<TR><TH colspan=${colspan}${tbc[0]}>■その他集計■</TH></TR>\n";
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
	print "<TR><TD colspan=${colspan}><DIV ALIGN=right><A HREF=\"$self\">[▲ メニューに戻る]</A></DIV></TD></TR></TABLE></CENTER><HR>\n\n";
}


### 生ログ
if (($P{MODE} eq 'rawlog') || ($P{MODE} eq 'all') || ($P{MODE} eq 'solo_rawlog') || ($P{MODE} eq 'solo_all')) {
	### 生ログのテーブル
	print "<CENTER>\n";
	foreach $filename (@filename) {
		if (defined($RAWLOG{$filename})) {
			print "<A NAME=rawlog_${filename}></A>\n<TABLE border=1 cellspacing=0 cellpadding=1${tbc[0]}><TR><TD><A HREF=\"#menu\"><B><FONT size=+1>生ログ ($filename.log)</FONT> / 最新$Limit_Log件</B></A></TD></TR><TR><TD><PRE>\n";
			print $RAWLOG{$filename};
			print "</PRE></TD></TR></TABLE><BR>\n";
		}
	}
	print "</CENTER>\n";
}


### カウント集計
if (($P{MODE} eq 'count') || ($P{MODE} eq 'all') || ($P{MODE} eq 'solo_analyze') || ($P{MODE} eq 'solo_all')) {
	print "<!-- カウント数集計 -->\n<CENTER>\n";
	print "<!-- 日別集計 -->\n<A name=day></A>\n";

	&Macro_PutTable_b(0, $koumoku{'day'}, \%DAY);
	undef %DAY;
	print "\n\n<BR>\n\n";
	print "<!-- 週別集計 -->\n<A name=weekly></A>\n";
	&Macro_PutTable_b(0, $koumoku{'weekly'}, \%WEEKLY);
	undef %WEEKLY;
	print "\n\n<BR>\n\n";
	print "<!-- 月別集計 -->\n<A name=month></A>\n";
	&Macro_PutTable_b(0, $koumoku{'month'}, \%MONTH);
	undef %MONTH;
	print "\n\n<BR>\n\n";
	print "<!-- 時間帯別集計 -->\n<A name=hour></A>\n";
	&Macro_PutTable_b(2, $koumoku{'hour'}, \%HOUR);
	undef %HOUR;
	print "\n\n<BR>\n\n";
	print "<!-- 曜日別集計 -->\n<A name=week></A>\n";
	&Macro_PutTable_b(2, $koumoku{'week'}, \%WEEK);
	undef %WEEK;
	print "\n\n<BR>\n\n";
	print "<!-- 年度別集計 -->\n<A name=year></A>\n";
	&Macro_PutTable_b(0, $koumoku{'year'}, \%YEAR);
	undef %YEAR;
	print "\n</CENTER><BR>\n\n";

	unless (($P{MODE} eq 'solo_analyze') || ($P{MODE} eq 'solo_all')) {
		print "<!-- サイト内ランキング -->\n<A name=rank></A>\n<CENTER><TABLE border=0 cellpadding=4><TR><TD valign=top>\n";
		&Macro_PutTable_a(0, '総合ランキング', 'ページ名', $COUNT_ALL,		'', 0, 0, \@rank_all);
		undef @rank_all;
		print "</TD><TD valign=top>\n";
		&Macro_PutTable_a(0, '月間ランキング', 'ページ名', $COUNT_MONTH,	'', 0, 0, \@rank_month);
		undef @rank_month;
		print "</TD></TR><TR><TD valign=top>\n";
		&Macro_PutTable_a(0, '週間ランキング', 'ページ名', $COUNT_WEEKLY,	'', 0, 0, \@rank_weekly);
		undef @rank_weekly;
		print "</TD><TD valign=top>\n";
		&Macro_PutTable_a(0, '本日ランキング', 'ページ名', $COUNT_DAY,		'', 0, 0, \@rank_day);
		undef @rank_day;
		print "</TD></TR></TABLE></CENTER><BR>\n\n";
	}
}

### 参照元系
if (($P{MODE} eq 'ref') || ($P{MODE} eq 'all') || ($P{MODE} eq 'solo_analyze') || ($P{MODE} eq 'solo_all')) {
	print "<!-- 参照元 -->\n<A name=ref></A>\n<CENTER>\n";
	&Macro_PutTable_a(0, '参照元統計', '参照元URL', $COUNT_REF, '', 0, $Limit_Ref, \@ref);
	undef @ref;
	print "</CENTER><BR>\n\n";
	print "<!-- サイト内移動分析 -->\n<A name=ref_own></A><CENTER>\n";
	&Macro_PutTable_a(2, 'サイト内移動分析', '移動の内訳', $COUNT_OWN, '自サイト内→自サイト内', $COUNT_OWN, 0, \@ref_own);
	undef @ref_own;
	print "</CENTER><BR>\n\n";

	print "<!-- サーチエンジン統計 -->\n<CENTER><TABLE border=0 cellpadding=8><TR><TD valign=top>\n<A name=search_share></A>\n";
	&Macro_PutTable_a(2, 'サーチエンジンシェア', '名前', $COUNT_SEARCH_SHARE, 'サーチエンジンから', $COUNT_SEARCH_SHARE, 0, \@ref_search_share);
	undef @ref_search_share;
	print "\n</TD><TD valign=top>\n<A name=search_key></A>\n";
	&Macro_PutTable_a(0, 'サーチエンジン分析', '検索ワード(概算)', $COUNT_SEARCH, '', 0, $Limit_Search, \@ref_search);
	undef @ref_search;
	print "\n</TD></TR></TABLE></CENTER>\n\n";
	print "<CENTER><TABLE border=0 cellpadding=8><TR><TD valign=top>\n<A name=tinami></A>\n";
	&Macro_PutTable_a(1, 'TINAMI分析', '検索ワード', $COUNT_TN, 'TINAMIから', $COUNT_TN_, $Limit_Tinami, \@ref_tinami);
	undef @ref_tinami;
	print "\n</TD><TD valign=top>\n<A name=sp></A>\n";
	&Macro_PutTable_a(1, 'Surfers Paradice分析', '検索ワード', $COUNT_SP, 'SPから', $COUNT_SP_, $Limit_Sp, \@ref_sp);
	undef @ref_sp;
	print "\n</TD></TR></TABLE></CENTER><BR>\n\n";
}

### ホスト系
if (($P{MODE} eq 'host') || ($P{MODE} eq 'all') || ($P{MODE} eq 'solo_analyze') || ($P{MODE} eq 'solo_all')) {
	print "<!-- ドメイン統計 -->\n<CENTER><TABLE border=0 cellpadding=8><TR><TD valign=top>\n<A name=host></A>\n";
	&Macro_PutTable_a(0, 'ドメイン別統計', 'ドメイン', $SAMPLES, '', 0, $Limit_Host, \@host);
	undef @host;
	print "\n</TD><TD valign=top>\n<A name=domain></A>\n";
	&Macro_PutTable_a(0, '国籍別統計', '国籍 (ccTLD)', $SAMPLES, '', 0, $Limit_Domain, \@host_dm);
	undef @host_dm;
	print "\n\n<BR>\n\n<A name=jp></A>\n";
	&Macro_PutTable_a(2, '国内ドメイン統計', '第2レベルドメイン', $COUNT_JP, '日本から', $COUNT_JP, 0, \@host_dm_jp);
	undef @host_dm_jp;
	print "\n\n<BR>\n\n<A name=us></A>\n";
	&Macro_PutTable_a(2, '米国ドメイン統計', '所属組織 (gTLD)', $COUNT_US, '米国から', $COUNT_US, 0, \@host_dm_us);
	undef @host_dm_us;
	print "\n</TD></TR></TABLE></CENTER><BR>\n\n";
}

### ブラウザ系
if (($P{MODE} eq 'ua') || ($P{MODE} eq 'all') || ($P{MODE} eq 'solo_analyze') || ($P{MODE} eq 'solo_all')) {
	print "<!-- ブラウザ統計 -->\n<CENTER><TABLE border=0 cellpadding=8><TR><TD valign=top>\n<A name=ua></A>\n";
	&Macro_PutTable_a(0, 'ブラウザ統計', 'エージェント名称', $SAMPLES, '', 0, $Limit_Agent, \@agent);
	undef @agent;
	print "\n</TD><TD valign=top>\n<A name=share_ie></A>\n";
	&Macro_PutTable_a(2, 'IE同士のシェア', 'IEバージョン', $COUNT_IE, 'IE総数', $COUNT_IE, 0, \@agent_ie);
	undef @agent_ie;
	print "\n\n<BR>\n\n<A name=share_nn></A>\n";
	&Macro_PutTable_a(2, 'NN同士のシェア', 'NNバージョン', $COUNT_NN, 'NN総数', $COUNT_NN, 0, \@agent_nn);
	undef @agent_nn;
	print "\n\n<BR>\n\n<A name=share_os></A>\n";
	&Macro_PutTable_a(0, '利用OS統計', 'OS種別(概算)', $COUNT_OS, '', 0, 0, \@agent_os);
	undef @agent_os;
	print "\n</TD></TR></TABLE></CENTER><BR>\n\n";
}

if (($P{MODE} eq 'screen') || ($P{MODE} eq 'all') || ($P{MODE} eq 'solo_analyze') || ($P{MODE} eq 'solo_all')) {
	print "<!-- 画面情報系 -->\n<CENTER><TABLE border=0 cellpadding=8><TR><TD valign=top>\n<A name=screen></A>\n";
	&Macro_PutTable_a(0, '画面情報統計', '画面情報', $COUNT_SCREEN, '', 0, 0, \@screen);
	undef @screen;
	print "\n</TD><TD valign=top>\n<A name=screen_size></A>\n";
	&Macro_PutTable_a(0, 'サイズ別統計', '横 x 縦', $COUNT_SCREEN_SIZE, '', 0, 0, \@screen_size);
	undef @screen_size;
	print "\n</TD><TD valign=top>\n<A name=screen_color></A>\n";
	&Macro_PutTable_a(0, '色深度別統計', '色数', $COUNT_SCREEN_COLOR, '', 0, 0, \@screen_color);
	undef @screen_color;
	print "\n</TD></TR></TABLE></CENTER><BR>\n\n";
}


### 計算時間測定終了
if ($DoPutBenchmark) {
	$CPU_end = (times)[0];
	printf("<DIV align=right>消費時間： %.3f CPU秒</DIV>\n",$CPU_end-$CPU_start);
}


;#--------------------------------------------------------------------
;#マクロ
;#--------------------------------------------------------------------
;### 生ログのリストを作るマクロ
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


;### 参照元をカウントするマクロ
sub Macro_CountRef {
	# サーチエンジンから
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


	# 通常のURL
	else {
		$flag = 0;
		$flg = 0;

		# 自サイトかチェック
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

	# サーチエンジンキーワード振り分け
	if ($flag > 0) {
		++$REF{'-search-'};
		split(/&/, $ref);
		foreach $_ (@_) {
			s/%20|\+|\|/ /gi;								# 処理速度の関係でかなり曖昧
#			s/%81@|%81b|\+|\|/ /gi;								# 処理速度の関係でかなり曖昧

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


;### ホスト名の形式を選別しカウントするマクロ
sub Macro_CountHost {
	split(/\./, $host);

	if (($host eq '') || ($host eq '-')) {						#'-'しかなかったら
		++$HOST_DM{'-'};
	}

	### FQDN
	elsif ($_[$#_] =~ /[a-z]$/) {
		## ccTLD
		if (length($_[$#_]) == 2) {
			++$HOST_DM{ $_[$#_] };
			$host = "*.$_[$#_-2].$_[$#_-1].$_[$#_]";

			# 日本は念入り
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


;### エージェント名を選別しカウントするマクロ
sub Macro_CountAgent {
	### Mozzila系
	if ($agent =~ /^!/) {
		$agent =~ '^!([\w.-]+)\s';					# NNのメジャーバージョンで統計
		$nnver = $1;

		$agent =~ /\((.*)\)/;						# 注釈情報を綿密に調べる準備
		split(/; /, $1);

		# IE系
		if ($_[0] =~ /^!([\w.-]+)/) {
			# NetCaptor
			if ($_[2] =~ /^NetCaptor/) {
				++$AGENT{'NetCaptor'};			
			}

			# 純IE
			else {
				++$AGENT{'Internet Explorer'};		# IE全体のシェア
				++$AGENT_IE{$1};					# IEのメジャーバージョン

				### IEの場合のOS統計
				if    ($_[1] eq 'Windows 98')     { ++$AGENT_OS{'Windows 98'}; }
				elsif ($_[1] eq 'Windows NT 5.0') { ++$AGENT_OS{'Windows 2000'}; }
				elsif ($_[1] eq 'Windows NT 5.1') { ++$AGENT_OS{'Windows XP'}; }
				elsif ($_[1] eq 'Windows NT 6.0') { ++$AGENT_OS{'Windows Vista'}; }
				elsif ($_[1] eq 'Windows 95')     { ++$AGENT_OS{'Windows 95'}; }
				elsif ($_[1] eq 'Windows NT 4.0') { ++$AGENT_OS{'Windows NT'}; }	# 多分
				elsif ($_[1] eq 'Windows NT')     { ++$AGENT_OS{'Windows NT'}; }
				elsif ($_[1] =~ /^MSN|^AOL/)      { ++$AGENT_OS{$_[2]}; }
				elsif ($_[1] eq 'Mac_PowerPC')    { ++$AGENT_OS{'Macintosh'}; }
				elsif ($_[1] eq 'Win32')          { ++$AGENT_OS{'Windows 95'}; }	# 多分
				elsif ($_[1] eq 'Windows 3.1')    { ++$AGENT_OS{'Windows 3.1'}; }
				# else { ++$AGENT_OS{'-etc-'}; print "$agent<BR>\n"; }
				#elsif ($_[1] =~ ".*Firefox/")	{++$AGENT{'Firefox'};
			}
		}


		# NN系
		elsif (($_[1] =~ /\bI\b/) || ($_[1] =~ /\bU\b/) || ($_[1] =~ /\bN\b/)) {
			++$AGENT{'Netscape Navigator'};		# NN全体のシェア
			++$AGENT_NN{$nnver};

			### OS統計
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
			# X端末の場合はもう少し仕分ける
			elsif ($_[0] eq 'X11')
				{ $_[2] =~ /^([^\s]+)/; ++$AGENT_OS{$1}; }
			# else { ++$AGENT_OS{'-etc-'}; print "$agent<BR>\n"; }
		}

		# その他コンパチ
		elsif ($_[0] eq 'compatible') {
			if ($_[1] =~ '^([^/]*)/.*') {		# ver.表記があるっぽい
				++$AGENT{$1};					# ver.表記を削る
			} else {
				++$AGENT{$_[1]};				# そのまま採用
			}
		}

		# そういうわけでもない微妙な立場のやつ
		else {
			if ($_[0] =~ "^DreamPassport/") {
				++$AGENT{'DreamPassport'};
			} elsif ($_[0] =~ "^PNWalker/") {
				++$AGENT{'PNWalker'};
			} elsif (($nnver == 3.01) && (!$_[1])) {	# CacheFlow
				++$AGENT{'CacheFlow'};
			} else {					# 本当にマイナー？
				++$AGENT{'-etc-'};
			}
		}
	}

	### Mozillaを名乗らない独立系
	else {
		if ($agent =~ '^([^/]*)/.*') {			# ver.表記があるっぽい
			++$AGENT{$1};						# ver.表記を削る
		} else {
			++$AGENT{$agent};					# そのまま採用
		}
	}
}


;### 画面情報をカウントするマクロ
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


;### コードや記号を意味ある文字列に変換する
sub Macro_ChangeList {
	### 参照元
	foreach (@ref) {
		($n, $data) = split(/\t/);

		if ($data eq '-') {
			$data = 'ブックマーク・お気に入りから / ロボット・巡回ソフト / URL直打ち / 参照元を隠蔽してのアクセス';
		} elsif ($data eq 'noscript') {
			$data = 'JavaScriptを禁止、又は使用出来ないブラウザにより参照元取得失敗';
		} elsif ($data eq '-own-') {
			$data = '自サイト内での移動';
		} elsif ($data eq '-search-') {
			$data = '(efStatに登録されている)サーチエンジンから';
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

	### サイト内移動分析
	&change_a(\@ref_own);

	### サーチエンジン
	&change_a(\@ref_search);

	### TINAMIカテゴリ
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


	### カントリーコード
	foreach (@host_dm) {
		($n, $data) = split(/\t/);

		if ($data eq 'ipaddr') {
			$data = "ドメイン判別できず (<B>IPアドレス</B>)";
		} elsif ($data eq '-') {
			$data = "<B><FONT SIZE=+1>[警告] IP記録無し</FONT><BR>(カウンタをTELNETから直接実行?)</B>";
		} elsif ($TABLE{'cctld'}{$data}) {
			$data = "$TABLE{'cctld'}{$data} (\*.<B>${data}<\/B>)";
		} else {
			$data = "未定義の国籍コード (*.<B>${data}<\/B>)";
		}

		$_ = "$n\t$data";
	}

	## 日本第2レベルドメイン
	foreach (@host_dm_jp) {
		($n, $data) = split(/\t/);

		if ($TABLE{'jpdomain'}{$data}) {
			$data = "$TABLE{'jpdomain'}{$data} (\*.<B>${data}<\/B>.jp)";
			$_ = "$n\t$data";
		}
	}

	## 米国第2レベルドメイン
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
			$data = "その他";
		} elsif ($data eq '-') {
			$data = "名称不明";
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


;### 出力用のテーブルを作る
;### 表示モード, 表題, 項目, 割る数, 副項目1, 副項目2(割る数), 表示下限, 表示させる配列
sub Macro_PutTable_a {
	my($mode, $title, $item, $div, $sub1, $sub2, $limit, $array) = @_;
	my($buf, $n, $data, $line, $ave, $width);

	unless (@$array == ()) {
		if (($sub2==0) || ($SAMPLES==0)) { $ave = 0; }							#0除算対策
		else { $ave = sprintf("%2.1f", ($sub2*100)/$SAMPLES); }

		### 表題
		print "<TABLE border=1 cellspacing=0 cellpadding=1${tbc[5]}>\n";

		print "\t<TR><TH nowrap colspan=2${tbc[0]}><A HREF=\"#menu\"><FONT size=+1>■ $title ■</FONT></A><BR>";
		if    ($mode == 0) { print "<FONT size=-1>(サンプル総数 : $div)</FONT>"; }																				#通常表示
		elsif ($mode == 1) { print "(<SUP>$sub1 : $sub2 ($ave%)</SUP> / <SUB>全体 : $SAMPLES</SUB>)<BR><FONT size=-1>(有効サンプル総数 : $div)</FONT>"; }		#TINAMI,SP分析用
		elsif ($mode == 2) { print "(<SUP>$sub1 : $sub2 ($ave%)</SUP> / <SUB>全体 : $SAMPLES</SUB>)"; }															#国内ドメイン,IEシェア,NNシェア用
		print "</TH></TR>\n";

		### 表の項目
		print "\t<TR><TH nowrap${tbc[1]}>件数</TH>";
		print "<TH${tbc[2]}>$item</TH></TR>\n";

		### 表の中身
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

		### 表示下限が指定されている場合、注釈を表示
		print "\t<TR><TD colspan=2 align=right${tbc[0]}><FONT size=-1><B>$limit件以下省略</B></FONT></TD></TR>\n" unless ($limit == 0);
		print "</TABLE>\n";
	}
}


;### カウンタ集計表 - 横置き
;### 表示タイプ, 項目種別, 連想配列
;### タイプ: 0=通常, 1=[サイト全体]がない, 2=[計]がない, 3=両方無い
sub Macro_PutTable_b {
	my($type, $ptr, $hash) = @_;
	my($colspan, @sum);

	if   (($type==2) || ($type==3)) {						#[ページ計]を表示しない
		$colspan = @$ptr;
	} else { $colspan = @$ptr+1; }

	### 項目(表題)
	print "<TABLE border=1 cellspacing=0 cellpadding=1${tbc[6]}>\n";
	print "\t<TR><TH colspan=${colspan}${tbc[0]}><A href=\"#menu\"><FONT size=+1>■ $ptr->[0] ■</FONT></A></TH></TR>\n";

	### 行 : 項目
	print "\t<TR${tbc[5]}><TH nowrap${tbc[1]}>　</TH>";
	for ($i=1 ; $i < @$ptr ; $i++) { print "<TH>$ptr->[$i]</TH>"; }
	### 列 : ページ計
	print "<TH${tbc[4]}>ページ計</TH>" unless (($type==2) || ($type==3));
	print "</TR>\n";

	### 行 : 内容
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
		### 列 : [ページ計]
		unless (($type==2) || ($type==3)) {
			print "<TH${tbc[8]}>$all</TH>";
		}
		print "</TR>\n";
	}

	### 行 : サイト全体
	unless (($type==1) || ($type==3)) {
		print "\t<TR align=right${tbc[7]}><TH nowrap${tbc[3]}>サイト計</TH>";
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
		### 列 : 検算部 ([ページ計] = [サイト計])
		printf("<TH%s>%d</TH>",${tbc[9]}, $all) unless ($type==2);
		print "<TR>\n";
	}

	print "</TABLE>\n";
}


;### カウンタ集計表 - 横置き
;### 表示タイプ, 項目種別, 表題, 単位, 項目数, 連想配列
;### タイプ: 0=通常, 1=[サイト全体]がない, 2=[計]がない, 3=両方無い
;### 個別モード: 0=通常, 1=曜日別集計, 2=月別集計
sub Macro_PutTable_c {
	my($type, $mode, $title, $sub, $max, $assoc_array) = @_;
	my($colspan, @sum, @d, @w);
	@w=('日','月','火','水','木','金','土');

	if   (($type==2) || ($type==3)) {						#[ページ計]を表示しない
		$colspan = $max+1;									# -> 列を減らす
	} else { $colspan = $max+2; }

	### 項目(表題)
	print "<TABLE border=1 cellspacing=0 cellpadding=1${tbc[6]}>\n";
	print "\t<TR><TH colspan=${colspan}${tbc[0]}><A href=\"#menu\"><FONT size=+1>■ $title ■</FONT></A></TH></TR>\n";

	### 行 : 項目
	print "\t<TR${tbc[5]}><TH nowrap${tbc[1]}>　</TH>";
	for ($i=0 ; $i < $max ; $i++) {
		print "<TH>";
		if    ($mode == 0) { print "$i$sub"; }				#通常
		elsif ($mode == 1) { print "$w[$i]$sub"; }			#曜日別集計
		elsif ($mode == 2) { printf("%d$sub", $i+1); }		#月別集計
		print "</TH>";
	}
	### 列 : ページ計
	unless (($type==2) || ($type==3)) { print "<TH${tbc[4]}>ページ計</TH>"; }
	print "</TR>\n";

	### 行 : 内容
	foreach $line (@filename) {
		print "\t<TR align=right><TH${tbc[2]}>$line</TH>";

		split(/\t/, $$assoc_array{ $line });

		for ($i=0 ; $i < $max ; $i++) {
			$_[$i] = &func::C62_Decode($_[$i]);
			print "<TD>$_[$i]</TD>";
			$sum[$i] += $_[$i];
		}
		### 列 : [ページ計]
		unless (($type==2) || ($type==3)) {
			printf("<TH%s>%d</TH>",${tbc[8]}, &func::CalcSum(@_));
		}
		print "</TR>\n";
	}

	### 行 : サイト全体
	unless (($type==1) || ($type==3)) {
		print "\t<TR align=right${tbc[7]}><TH nowrap${tbc[3]}>サイト計</TH>";
		for ($i=0 ; $i < $#sum+1 ; $i++) { print "<TH>$sum[$i]</TH>"; }
		### 列 : 検算部 ([ページ計] = [サイト計])
		unless ($type==2) { printf("<TH%s>%d</TH>",${tbc[9]}, &func::CalcSum(@sum)); }
		print "<TR>\n";
	}

	print "</TABLE>\n";
}
1;
