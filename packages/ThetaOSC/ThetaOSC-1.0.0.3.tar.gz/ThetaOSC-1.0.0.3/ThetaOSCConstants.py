"""
Name	Type	Description
sessionId 	String 	現在のセッションID
batteryLevel 	Number 	バッテリー残量
（0.0、0.33、0.67、1.0の4段階）
storageChanged 	Boolean 	新しい形式のストレージの挿入／取り外しの有無
_captureStatus 	String 	連続撮影状態
"shooting"、"idle"、
"self-timer countdown"(ファームウェア01.42以降)
（shooting: 連続撮影中、idle: 撮影待機中、
self-timer countdown: セルフタイマー作動中）
_recordedTime 	Number 	撮影中動画の撮影時間（秒）
_recordableTime 	Number 	撮影中動画の残り撮影時間（秒）
_latestFileUri 	String 	最後に保存されたファイルのID
_batteryState 	String 	充電状態
"charging"、"charged"、"disconnect"
（charging: 充電中、charged: 充電完了、
  disconnect: 充電していない）
_cameraError 	String Array 	カメラ本体のエラー情報（詳細は次項）
"""


class _cameraError:
    """
Event flag	Error code	Desription
0x00000001 	NO_MEMORY 	メモリー容量不足
0x00000002 	WRITING_DATA 	データ書き込み中
0x00000004 	FILE_NUMBER_OVER 	ファイル番号の制限を超えている
0x00000008 	NO_DATE_SETTING 	カメラの内蔵時計が未設定
0x00000010 	COMPASS_CALIBRATION 	電子コンパスに誤差が発生
0x00000100 	CARD_DETECT_FAIL 	ＳＤメモリカードが未装着
0x00400000 	CAPTURE_HW_FAILED 	撮影系ハードウェアの異常検出
0x01000000 	CANT_USE_THIS_CARD 	メディア不良
0x02000000 	FORMAT_INTERNAL_MEM 	内蔵メモリのフォーマットエラー
0x04000000 	FORMAT_CARD 	ＳＤメモリカードのフォーマットエラー
0x08000000 	INTERNAL_MEM_ACCESS_FAIL 	内蔵メモリのアクセスエラー
0x10000000 	CARD_ACCESS_FAIL 	ＳＤメモリカードのアクセスエラー
0x20000000 	UNEXPECTED_ERROR 	未定義エラー
0x40000000 	BATTERY_CHARGE_FAIL 	充電異常
0x80000000 	HIGH_TEMPERATURE 	温度異常
    """

class OSCerror:
    """
    Error code	HTTP
    Status code	Description
    unknownCommand 	400 	不正なコマンドの発行
    disabledCommand 	403 	カメラ本体の状態によりコマンドが実行不可
    missingParameter 	400 	コマンド発行時の必須パラメータが不足
    invalidParameterName 	400 	パラメータ名やオプション名が不正
    invalidSessionId 	403 	コマンド発行時のsessionIdが不正
    invalidParameterValue 	400 	コマンド発行時のパラメータ値が不正
    corruptedFile 	403 	破壊ファイルに対する処理要求
    cameraInExclusiveUse 	400 	カメラが排他利用されているためセッション開始不可
    powerOffSequenceRunning 	403 	電源オフ中の処理要求
    invalidFileFormat 	403 	無効なファイルフォーマットの指定
    seviceUnavailable 	503 	一時的な処理要求の受付不可
    canceledShooting 	403 	セルフタイマーでの撮影要求キャンセル
    camera.takePictureのCommands/Statusで返される
    (ファームウェアv01.42以降)
    unexpected 	503 	その他のエラー
    """
