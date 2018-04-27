#!/usr/bin/perl
require 5.004;   # 本プログラムは(少なくとも)perl 5.004以上を必要とします。
$ver = '2.1.2';  # 本プログラムの版数。禁変更。
;#+------------------------------------------------------------------------
;#|efCount[efStatカウンタ部]
;#|(C)1998-2000 不可思議絵の具(http://yugen.main.jp/)
;#+------------------------------------------------------------------------
;# ☆☆☆ 共通の設定項目(必要) ☆☆☆
;#+------------------------------------------------------------------------
;# [動作モード]
;# SSIとして動作させるなら 1 ， CGIとして動作させるなら 0 。
$USER{'SSIMode'} = 0;

;# [ログファイルを格納したディレクトリの名前]
;# ログ用ディレクトリは fstat/ 以下に作って下さい。
$USER{'DIR_Log'} = 'log';

;# [アクセスログ最大保存数]
;# 1以上、3000未満の数値を入力して下さい。
$USER{'MaxLog'} = 1000;

;# [再読み込み防止機構(IPチェック)を利用するか]
;# 1 = する(デフォルト) / 0 = しない(重複カウントを許す)
$USER{'IPCheck'} = 1;

    ;# (IPCheckが１の場合有効)
    ;# [再読み込み防止機構の有効期限] (分単位で指定)
    ;# 指定した時間が経つと、同じIPであってもカウントします。
    ;# 0を指定すると、同じIPの間はずっとカウントしません。
    $USER{'IPExpire'} = 0;

# [カウントアップさせないホスト名・IPアドレス]
# 複数指定できますが、完全一致しなければなりません。
# ここを空欄にしてはいけません。　適当で良いですから埋めて下さい。
@USER_DenyIP = (
	'165.93.96.101',
	'abc123.ppp.test.ne.jp',
);

# [カウントアップさせないブラウザ]
# 複数指定できます。　前方比較を行います。
# ここを空欄にしてはいけません。　適当で良いですから埋めて下さい。
@USER_DenyAgent = (
	'WWWC',
	'Kerberos',
	'Monazilla',
);


;#+------------------------------------------------------------------------
;# ☆☆☆ CGIとして使うときの設定項目 ☆☆☆
;#+------------------------------------------------------------------------
;# [カウンタ用画像を格納したディレクトリの名前]
;# カウンタ画像用ディレクトリは fstat/ 以下に作って下さい。
$USER{'Dir_Img'} = 'image';

	;# [カウンタのイメージの名前(デフォルトで使用する物)]
	$USER{'DigitName'} = 'fuksan';


;#+------------------------------------------------------------------------
;# ☆☆☆ SSI として使うときの設定項目 ☆☆☆
;#+------------------------------------------------------------------------
;# [efStat一式を格納したディレクトリ]
;# ※呼び出すHTMLから見た相対パスでも良いが、ルートからのフルパスが望ましい。
;# ※最後のスラッシュ(/)は必ず必要。
$USER{'SSI_Pass'} = '/home/sites/home/users/fuka/web/cgi-bin/fstat/';


;#+------------------------------------------------------------------------
;# ☆☆☆ その他、補助的な項目 ☆☆☆
;#+------------------------------------------------------------------------
# [gifcat.plのありか (通常は変更しないで下さい)]
$USER{'GifCat'} = './lib/gifcat.pl';


#+------------------------------------------------------------------------
# (設定ここまで)
#+------------------------------------------------------------------------
# ※ここからは分かる人だけ弄って下さい。
# 　(タブのサイズ・[4]、折返し・[無し]で綺麗に表示されます)
#+------------------------------------------------------------------------
#|&main
#+------------------------------------------------------------------------
&Macro_Setup;				# 各種初期化
&Macro_Access;				# アクセス記録
&Macro_LoadData;			# ログファイルを読み込み
&Macro_Check;				# チェック
if ($OutputOnly) {			# 重複アクセスは記録しない
	&Macro_Output;			# 結果を出力
} else {
	&Macro_Count;			# カウント
	&Macro_SaveData;		# 保存
	&Macro_Output;			# 結果を出力
}
exit;


#+------------------------------------------------------------------------
#|プログラムの流れとしてのサブルーチン
#+------------------------------------------------------------------------
### 各種初期化
sub Macro_Setup {
	$ENV{'TZ'} = 'JST-9';													# 環境変数TZを日本時間に設定
	$Digit = 0;
	$OutputOnly = 0;														# 1=出力のみ

	### 現在時刻の取得
	$RUN_TIME   = time;														# 現在時刻(秒形式)
	@RUN_TIME   = localtime($RUN_TIME);										# 現在時刻(変換後)
	$RUN_TIME_E = &C62_Encode($RUN_TIME);									# エンコード済現在時刻
	$RUN_week   = &TotalWeek($RUN_TIME[7]);									# 現在週

	### 引数の解釈
	foreach $data (split(/&/, $ENV{'QUERY_STRING'})) {
		($key , $val) = split(/=/,$data);
		$P{$key} = $val;
	}
	$Filename = $P{'LOG'};													# ログファイル名

	## SSIモード
	if ($USER{'SSIMode'}) {
		$USER{'DIR_Log'} = "${USER{'SSI_Pass'}}${USER{'DIR_Log'}}/";		# ログ格納ディレクトリ

		# 動作モード
		if    ($P{'MODE'} eq '-') { $OutputOnly = 1; } 						# "-"ならカウント無し
		elsif ($P{'MODE'} eq 'h') { $OutMode = 'h' ; }						# "h"なら出力無し
	}

	## CGIモード
	else {
		# 動作モード
		if ($P{'MODE'} =~ /^-([atyw])$/) {									# 頭に - があれば出力のみ
			$OutMode = $1;
			$OutputOnly = 1;
		} elsif ($P{'MODE'} =~ /^([atyw])$/) {								# 無ければ普通にチェック
			$OutMode = $1;
		} else { $OutMode = 'a'; }											# 満たさなければ強制的に a に

		if ($P{'DIGIT'} > 20) { &Macro_PutError('e0001'); }					# 桁数
		else                  { $Digit = $P{'DIGIT'}-1; }

		$ENV{'HTTP_REFERER'} = $P{'REF'};									# 参照元

		$screen = $P{'SCR'};												# 画面情報

		$USER{'DigitName'} = $P{'FONT'} if ($P{'FONT'} ne '');				# フォント名

		## ディレクトリ名を修正
		$USER{'DIR_Log'} = "./${USER{'DIR_Log'}}/";							# ログ格納ディレクトリ
		$USER{'Dir_Img'} = "./${USER{'Dir_Img'}}/${USER{'DigitName'}}/";	# フォント格納ディレクトリ

		### 時刻表示モードだったらここで終わり
		if ($OutMode eq 'w') {
			$Digit = 0;
			print &Func_PutGIF(sprintf("%02dc%02d", $RUN_TIME[2], $RUN_TIME[1]));
			exit(0);
		}
	}
}


### [アクセス記録]
sub Macro_Access {
	### 訪問者のリモートホスト取得
	$host = $ENV{'REMOTE_ADDR'};

	if ($host eq '') {
		$host = '-';
	} else {
		# proxyチェック
		$host = $1 if ($ENV{'HTTP_FORWARDED'} =~ / for (.*)/);		# HTTP_FORWARDED (DeleGate , Squid)

		# IP -> HOST
		$host = gethostbyaddr(pack("C4", split(/\./, $host)), 2) || $host;
	}

	### ユーザエージェント取得
	$agent = $ENV{'HTTP_USER_AGENT'};
	$agent = 'Monazilla/1.0' if ($agent =~ /Seven\//);
	$agent =~ s'^Mozilla/'!';
	$agent =~ s"\(compatible; MSIE (.+)\)"(!$1)";
	$agent = '-' if ($agent eq '');								#エージェント名がなければ'-'に置き換える

	### 参照元取得
	$ref = $ENV{'HTTP_REFERER'};
	$ref =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack("C",hex($1))/ge;	# URLDecode
	$ref =~ s/\?$//;
	$ref =~ s"(/index\.)html$|\1htm$|\1shtml$|\1php3$"/"i;
	$ref =~ s'^http://'!'i;
	if (($ref eq '') || ($ref eq '[unknown origin]') ||			# リンク元無し, '[unknown origin]', 'bookmark'なら'-'に置き換える
	    ($ref eq 'bookmarks') || ($ref eq "',ref,'"))
	{ $ref = '-'; }

	### 画面モード
	if (($screen eq '') || ($screen !~ /^[0-9]/)) {
		$screen = '-';
	} else {
		($screen_x, $screen_y, $screen_color) = split(/,/, $screen);
		$screen_x		= &C62_Encode($screen_x);
		$screen_y		= &C62_Encode($screen_y);
		$screen_color	= &C62_Encode($screen_color);
		$screen = "$screen_x,$screen_y,$screen_color";
	}
}


### [ログファイルを読み込み]
sub Macro_LoadData {
	unless (open(LOG,"+<${USER{'DIR_Log'}}${Filename}.log")) {
		&Macro_PutError('e0000');
	}
	flock(LOG,2);
	for ($i=0 ; $i<8 ; $i++) { chomp($count[$i] = <LOG>); }		# 各種カウント数
	chomp(@log = <LOG>);										# アクセスログ

	###新規ログならフォーマット
	if ($count[0] eq '') {
		$count[0] = "FC2\t${RUN_TIME_E}";
		$count[1] = "${RUN_TIME_E}\t0";
		$count[2] = "0\t0\t0\t0\t0\t0\t0\t0";
		$count[3] = "0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0";
		$count[4] = "0\t0\t0\t0\t0\t0\t0";
		$count[5] = "0\t0\t0\t0\t0\t0";
		$count[6] = "0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0";
		$count[7] = "0\t0\t0\t0\t0\t0";
	}

	# 旧形式のログなら変換
	elsif ($count[0] !~ /^FC2/) {
		&Macro_Convert;
	}

	###データを各配列に格納
	($LOG_ID, $LOG_SINCE_E)			= split(/\t/, $count[0]);		#ヘッダ
	$LOG_SINCE						= &C62_Decode($LOG_SINCE_E);
	&Macro_PutError('e1110') if ($LOG_ID ne 'FC2');					# ログ形式check(機能しない?)

	($LOG_TIME_E, $ALL_E, $LOG_IP)	= split(/\t/, $count[1]);		# 各種情報
	$LOG_TIME						= &C62_Decode($LOG_TIME_E);
	$ALL							= &C62_Decode($ALL_E);

	@DAILY							= &split($count[2]);			# 日別集計
	@HOUR							= &split($count[3]);			# 時間別集計
	@YOUBI							= &split($count[4]);			# 曜日別集計
	@WEEK							= &split($count[5]);			# 週別集計
	@MONTH							= &split($count[6]);			# 月別集計
	@YEAR							= &split($count[7]);			# 月別集計

	# ログの日付を求める
	@LOG_TIME = localtime($LOG_TIME);
	$LOG_week = &TotalWeek($LOG_TIME[7]);

	# 文字列を切り分け、10進数に戻す
	sub split {
		my($str) = @_;
		my(@array);

		@array = split(/\t/, $str);
		foreach (@array) { $_ = &C62_Decode($_); }
		return @array;
	}
}


### カウントすべき訪問者かチェック
sub Macro_Check {
	if ($USER{'IPCheck'}) {												# 重複カウントを許すか？
		if ($host eq $LOG_IP) {											# 前回訪問者と同じか？
			if ($USER{'IPExpire'} == 0) {
				$OutputOnly = 1;
			} else {
				if ($RUN_TIME - $LOG_TIME < $USER{'IPExpire'} * 60) {	# IPは有効期限外か？
					$OutputOnly = 1;
				} else { $OutputOnly = 0; }
			}
		} else { $OutputOnly = 0; }
	} else { $OutputOnly = 0; }

	foreach (@USER_DenyIP) {											# 弾くべきIPか？
		if ($host eq $_) {
			$OutputOnly = 1;
			last;
		}
	}

	foreach (@USER_DenyAgent) {											# 弾くべきブラウザか？
		if ($agent =~ /^$_/) {
			$OutputOnly = 1;
			last;
		}
	}
}


### [カウントする]
sub Macro_Count {
	my($n);

	### 何日間経過したか求める
	$n  = $RUN_TIME[7] - $LOG_TIME[7];
	$n += 366 if ($n < 0);			# 年が明けた場合補正(n+366日経過)

	if ($n == 0) { $DAILY[0]++; }	# 同じ日
	elsif ($n > 0) {				# n日経過
		for (1 .. $n) { unshift(@DAILY, 0); }
		$DAILY[0] = 1;
	}

	### 何週間経過したか求める
	$n  = $RUN_week - $LOG_week;
	$n += 53 if ($n < 0);			# 年が明けた場合補正(n+53週間経過)

	if ($n == 0) { $WEEK[0]++; }	# 同じ週
	elsif ($n > 0) {				# n週間経過
		for (1 .. $n) { unshift(@WEEK, 0); }
		$WEEK[0] = 1;
	}


	### 何年間経過したか求める
	$n = $RUN_TIME[5] - $LOG_TIME[5];

	if (($n == 0) || ($n < 0)) { $YEAR[0]++; }	# 同じ年(サーバ側時計が古い場合もこの処理)
	elsif ($n > 0) {							# n年経過
		@MONTH = (0) x 12;						# 月別集計をreset
		for (1 .. $n) { unshift(@YEAR, 0); }
		$YEAR[0] = 1;
	}

	++$ALL;
	++$HOUR [ ${RUN_TIME[2]} ];
	++$YOUBI[ ${RUN_TIME[6]} ];
	++$MONTH[ ${RUN_TIME[4]} ];
}


### [カウント結果を配列に格納]
sub Macro_SaveData {
	$ALL_E = &C62_Encode($ALL);

	$count[0] = "FC2\t$LOG_SINCE_E";									# 各種情報
	$count[1] = "$RUN_TIME_E\t$ALL_E\t$host";							# 各種情報
	$count[2] = &Func_Array2Str(8,  \@DAILY);							# 日別集計
	$count[3] = &Func_Array2Str(24, \@HOUR);							# 時間別集計
	$count[4] = &Func_Array2Str(7,  \@YOUBI);							# 曜日別集計
	$count[5] = &Func_Array2Str(6,  \@WEEK);							# 週別集計
	$count[6] = &Func_Array2Str(12, \@MONTH);							# 月別集計
	$count[7] = &Func_Array2Str(6,  \@YEAR);							# 月別集計
	$new_log  = "$ALL_E\t$RUN_TIME_E\t$host\t$agent\t$ref\t$screen";	#新規ログ行

	unshift(@log, $new_log);											# 新しいログを付け足し、
	splice(@log, $USER{'MaxLog'});										# 古いログは消し去る

	seek(LOG,0,0);

	foreach (@count) { print LOG "$_\n"; }
	foreach (@log)   { print LOG "$_\n"; }

	truncate(LOG,tell);

	flock(LOG,8);
	close(LOG);

	### 配列の内容を一行の文字列に直す関数
	### $limitより大きなデータは切り捨てる
	sub Func_Array2Str {
		my($limit, $array) = @_;
		splice(@$array, $limit);

		foreach (@$array) { $_ = &C62_Encode($_); }
		return join("\t", @$array);
	}
}


### [カウント数出力]
sub Macro_Output {
	my($s, $m, $h, $d, $mo, $y, $w) = @RUN_TIME;
	my($today, $yesterday) = @DAILY;
	my($all) = $ALL;
	my(@w);

	unless ($OutputOnly) {
		$today      = &C62_Decode($today);
		$yesterday  = &C62_Decode($yesterday);
	}

	### SSIモードなら
	if ($USER{'SSIMode'}) {
		print "Content-type: text/plain\n\n";
		if ($OutMode ne 'h') {
			$agent =~ s'^!'Mozilla/';
			$agent =~ s"\(!(.+)\)"(compatible; MSIE $1)";
			$ref   =~ s'^!'http://';
			++$mo;
			$y += 1900;

			;#+--[ * メッセージ(ユーザ変更可) * ]------------[ ここから ]-+

			# 好きな曜日の表記を選んで下さい。
			@w = ('日', '月','火','水','木','金','土');  $w = $w[$w];
			# @w = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');  $w = $w[$w];

			;#+-----------------------------------------------------------+
			;#(メッセージ中の変数の意味)
			;#  ${all}      …総ヒット数    ${y} …年    ${h}…時
			;#  ${today}    …本日ヒット数  ${mo}…月    ${m}…分
			;#  ${yesterday}…昨日ヒット数  ${d} …日    ${s}…秒
			;#  ${host}     …訪問者ホスト  ${w} …曜日
			;#  ${agent}    …ブラウザ名
			;#  ${ref}      …参照元        ※ " は \" に置き換えましょう！
			;#+-----------------------------------------------------------+

			@mes = (
				#"${all}\n${today}\n${yesterday}\n${host}\n${agent}\n${ref}\n${y}年${mo}月${d}日(${w})\n${h}時${m}分${s}秒\n",
				"<FONT FACE=\"Arial\">Total:<B>${all}</B> / Today:<B>${today}</B> / Yesterday:<B>${yesterday}</B></FONT>",
				#"<FONT SIZE=+1><B>ぴぃ～かぁ～☆</B></FONT>　全部で<B>${all}万ボルト</B>・今日は<B>${today}万ボルト</B>・昨日は<B>${yesterday}万ボルト</B>の蓄電",
				#"艦長ぉ！　前方に機影確認！相手識別番号<B>${host}</B>っ！<BR>敵機です！ コンディション・レッドッッッ！！<BR>その数、前方に<B>${all}機</B>ッ！　左舷に<B>${today}機</B>！　右舷に<B>${yesterday}機</B>！　波動砲用意しますか!?(古)",
			);

			;#+--[ * メッセージ(ユーザ変更可) * ]------------[ ここまで ]-+

			# ランダムに選ぶ
			srand(time + $$);
			$n = int(rand($#mes+1));

			# 表示
			print $mes[$n];
		}
	}

	### CGIモードなら
	else {
		# 総アクセス数
		if    ($OutMode eq 'a') { print &Func_PutGIF($all); }
		# 今日アクセス数
		elsif ($OutMode eq 't') { print &Func_PutGIF($today); }
		# 昨日アクセス数
		elsif ($OutMode eq 'y') { print &Func_PutGIF($yesterday); }
	}
}


### [gifを出力]
sub Func_PutGIF {
	my($Data) = @_;
	my($i, $n, @array);

	require $USER{'GifCat'};
	print "Content-type: image/gif\n";
	print "Expires: 01/01/1970 00:00:00 JST\n\n";	# キャッシュを無効にする
	binmode(STDOUT);

	### 桁数を指定されたら、足りない分を0で補う
	$Data = ('0'x($Digit-(length($Data)-1))).$Data if (length($Data)-1 < $Digit);

	for ($i=0 ; $i < length($Data) ; $i++) {
		$n = substr($Data, $i, 1);
		push(@array, "${USER{'Dir_Img'}}${n}${USER{'DigitName'}}.gif");
	}

	return &gifcat'gifcat(@array);
}


### [エラー出力]
# e0000 = ファイルオープン失敗
# e0001 = 桁数あふれ
# e1110 = ログの形式が不正
# e1111 = 無効なオプション
sub Macro_PutError {
	my($code) = @_;

	if ($USER{'SSIMode'}) {
		print "Content-type: text/plain\n\n";
		if ($code eq 'e0000') {
			print "<P><B>[efCount $ver(SSI)]ログを開くことが出来ませんでした</B><br>${USER{'DIR_Log'}}${Filename}.log</P>\n";
		} elsif ($code eq 'e1110') {
			print "<P><B>[efCount $ver(SSI)]ログの形式が不正です</B></P>\n";
		} elsif ($code eq 'e1111') {
			print "<P><B>[efCount $ver(SSI)]無効なオプションです</B></P>\n";
		} else {
			print "<P><B>[efCount $ver(SSI)]未定義のエラーです</B></P>\n";
		}
	} else {
		require $USER{'GifCat'};
		print "Content-type: image/gif\n\n";
		binmode(STDOUT);
		for ($i=0 ; $i < length($code) ; $i++) {
			$n = substr($code, $i, 1);
			push(@Digit, "./lib/${n}.gif");
		}
		print &gifcat'gifcat(@Digit);
	}
	exit(1);
}


sub Macro_Convert {
	my($num, $time, $host, $agent, $ref, $screen,
	   $day, $week, $time, $all,   $ip,  $i,      @work);

	for ($i = 1; $i < 6; $i++) {
		split(/#/, $count[$i]);
		foreach (@_) { $_ = &C62_Encode($_); }
		$count[$i] = join("\t", @_);
	}

	($day, $week, $time, $all, $ip) = split(/#/, $count[0]);

	$all_e = &C62_Encode($all);

	# カウント記録部の変換
	# 一旦作業用配列に入れる
	$work[0] = "FC2\t${RUN_TIME_E}";
	$work[1] = "${RUN_TIME_E}\t${all_e}\t${ip}";
	$work[2] = $count[1];
	$work[3] = $count[2];
	$work[4] = $count[3];
	$work[5] = $count[4];
	$work[6] = $count[5];
	$work[7] = "0\t0\t0\t0\t0\t0";
	unshift(@log,$count[6]);	# 溢れて読み込まれたアクセスログ
	@count = @work;				# 引っ越す

	# ログ記録部の変換
	foreach (@log) {
		($num, $time, $host, $agent, $ref, $screen) = split(/#/, $_);
		$num   = &C62_Encode($num);
		$time  = &C62_Encode($time);
		$agent =~ s/%23/#/g;
		$agent =~ s'^Mozilla/'!';
		$agent =~ s"\(compatible; MSIE (.+)\)"(!$1)";
		$ref   =~ s'^http://'!'i;
		$_     = "$num\t$time\t$host\t$agent\t$ref\t$screen";
	}
}


### 通算週を求める関数
sub TotalWeek {
	my($total) = @_;
	my($week);

	if ($total < 7) { $week = 0; }				# 0除算対策
	else            { $week = int($total/7); }

	return $week;
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
