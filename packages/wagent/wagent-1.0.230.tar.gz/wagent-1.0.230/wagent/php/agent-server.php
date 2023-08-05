<?php
require_once ('wagent-prot.php');
require_once ('check_file.php');
require_once ('external/sockets/src/Exception/SocketException.php');
require_once ('external/sockets/src/Socket.php');
require_once ('external/sockets/src/Server.php');

use Navarr\Socket\Exception\SocketException;
use Navarr\Socket\Socket;
use Navarr\Socket\Server;



class AgentServer extends Server
{
    const AUTOREPLY_NONE = 1;
    const AUTOREPLY_DELIVERED = 2;
    const AUTOREPLY_READ = 3;

    const PENDIND_EVENTS_FILE = 'pending_events.dat';

    const MAXREAD_LINE = 4096;

    private $wa = null;
    private $registration = null;
    private $number = null;
    private $eventQueue = null;
    private $timeStart = 0;
    private $idleTimeout = 0;
    private $everPolledMessages = false;
    private $forcedEventFlushed = true;
    private $isCleaningUp = false;
    private $isActive = false;
    private $nickname = '';
    private $autoReplyMode = AgentServer::AUTOREPLY_DELIVERED;
    private $debug = false;

    function _debug_print($data)
    {
        if (!$this->debug)
            return;

        $result = print_r($data, true);
        print ('[agent-server][debug] ===(' . $result .")===\n");
    }

    private function CheckExtensions ()
    {
        if (!extension_loaded('sqlite3'))
            throw new Exception ('Missing sqlite3 extension');
        if (!extension_loaded('PDO') || !extension_loaded('pdo_sqlite'))
            throw new Exception ('Missing PDO and pdo_sqlite extension');
        if (!extension_loaded('mcrypt'))
            throw new Exception ('Missing mcrypt extension');
        if (!extension_loaded('protobuf'))
            throw new Exception ('Missing protobuf extension');
        if (!extension_loaded('curve25519'))
            throw new Exception ('Missing curve25519 extension');
    }

    private function Initialize ($number, $nickname, $autoReplyMode = AgentServer::AUTOREPLY_DELIVERED)
    {
        $this->_debug_print ('Initialize...');
        $this->_debug_print ($number);
        $this->_debug_print ($nickname);
        $this->_debug_print ($autoReplyMode);

        if ($this->IsInitialized())
            return;

        $this->CheckExtensions ();

        $readReceipt      = false;
        $deliveredReceipt = false;

        if ($autoReplyMode == AgentServer::AUTOREPLY_NONE) {
            $readReceipt = false;
            $deliveredReceipt = false;
        }
        if ($autoReplyMode == AgentServer::AUTOREPLY_DELIVERED) {
            $readReceipt = false;
            $deliveredReceipt = true;
        }
        if ($autoReplyMode == AgentServer::AUTOREPLY_READ) {
            $readReceipt = true;
            $deliveredReceipt = true;
        }

        $this->number = $number;
        $this->nickname = $nickname;
        $this->autoReplyMode = $autoReplyMode;

        if ($this->eventQueue == null)
            $this->eventQueue = new SplQueue();

        $this->wa = new WagentProt($number, $nickname, /* debug output */ $this->debug);
        $this->wa->enableReadReceipt($readReceipt);
        $this->wa->enableDeliveredReceipt($deliveredReceipt);

        $this->BindEvents ();
        $this->RestorePendingEvents();
    }

    function GetRegistration ()
    {
        if ($this->number == null)
            return null;
        if ($this->registration == null)
            $this->CreateRegistration();
        return $this->registration;
    }

    function LiteConnect ($number)
    {
        $this->number = $number;
        $this->CreateRegistration();
    }

    function Connect ($number, $nickname, $autoReplyMode = AgentServer::AUTOREPLY_DELIVERED)
    {
        $id = 'onconnect';

        $this->Initialize ($number, $nickname, $autoReplyMode);
        $this->wa->connect();

        return $this->GetEventResult ($id);
    }

    function PushEvent ($eventName, $eventData)
    {
        $item ['name'] = $eventName;
        $item ['data'] = $eventData;
        $this->eventQueue->enqueue($item);
    }

    function PopEvent ()
    {
        if ($this->eventQueue->isEmpty())
            return null;
        return $this->eventQueue->dequeue ();
    }

    function Close ()
    {
        if ($this->wa != null) {
            $this->wa->disconnect();
            $this->isActive = false;
        }
    }

    function Login ($password)
    {
        try {
            $this->wa->loginWithPassword ($password);
            return true;
        } catch (LoginFailureException $e) {
            $this->_debug_print('Login failed...');
            $this->_debug_print($e);
            return false;
        }
    }

    function ParseID ($jids)
    {
        if (!is_array($jids))
            return WagentProt::ParseID ($jids);

        $result = [];
        foreach ($jids as $key => $jid) {
            $result[$key] = WagentProt::ParseID ($jid);
        }
        return $result;
    }

    public function OnCredentialsBad ($phoneNumber, $status, $reason, $id)
    {
        $params ['status'] = $status;
        $params ['reason'] = $reason;
        $params ['code'] = '403';
        $params ['id'] = $id;
        $this->PushEvent('oncredentialsbad', $params);
    }

    public function OnCredentialsGood ($phoneNumber, $login, $pw, $type, $expiration, $kind, $price, $cost, $currency, $price_expiration, $id)
    {
        $params ['login'] = $login;
        $params ['pw'] = $pw;
        $params ['type'] = $type;
        $params ['expiration'] = $expiration;
        $params ['kind'] = $kind;
        $params ['price'] = $price;
        $params ['cost'] = $cost;
        $params ['currency'] = $currency;
        $params ['price_expiration'] = $price_expiration;
        $params ['id'] = $id;
        $this->PushEvent('oncredentialsgood', $params);
    }

    public function OnCodeRegisterFailed ($phoneNumber, $status, $reason, $retry_after, $id)
    {
        $params ['id'] = $id;
        $params ['status'] = $status;
        $params ['reason'] = $reason;
        $params ['retry_after'] = $retry_after;
        $params ['code'] = '403';
        $this->PushEvent('oncoderegisterfailed', $params);
    }

    public function OnCodeRegister ($phoneNumber, $login, $pw, $type, $expiration, $kind, $price, $cost, $currency, $price_expiration, $id)
    {
        $params ['id'] = $id;
        $params ['login'] = $login;
        $params ['pw'] = $pw;
        $params ['type'] = $type;
        $params ['expiration'] = $expiration;
        $params ['kind'] = $kind;
        $params ['price'] = $price;
        $params ['cost'] = $cost;
        $params ['currency'] = $currency;
        $params ['price_expiration'] = $price_expiration;
        $this->PushEvent('oncoderegister', $params);
    }

    public function OnCodeRequestFailedTooRecent ($phoneNumber, $method, $reason, $retry_after, $id)
    {
        $params ['id'] = $id;
        $params ['method'] = $method;
        $params ['reason'] = $reason;
        $params ['code'] = '400';
        $params ['retry_after'] = $retry_after;
        $this->PushEvent('oncoderequestfailedtoorecent', $params);
    }

    public function OnCodeRequestFailedTooManyGuesses ($phoneNumber, $method, $reason, $retry_after, $id)
    {
        $params ['id'] = $id;
        $params ['method'] = $method;
        $params ['reason'] = $reason;
        $params ['retry_after'] = $retry_after;
        $params ['code'] = '401';
        $this->PushEvent('oncoderequestfailedtoomanyguesses', $params);
    }

    public function OnCodeRequestFailed ($phoneNumber, $method, $reason, $param, $id)
    {
        $params ['id'] = $id;
        $params ['method'] = $method;
        $params ['reason'] = $reason;
        $params ['param'] = $param;
        $params ['code'] = '401';
        $this->PushEvent('oncoderequestfailed', $params);
    }

    public function OnCodeRequest ($phoneNumber, $method, $length, $id)
    {
        $params ['id'] = $id;
        $params ['method'] = $method;
        $params ['length'] = $length;
        $this->PushEvent('oncoderequest', $params);
    }

    public function OnWhatsAppConnectSuccess($phoneNumber, $socket)
    {
        $this->_debug_print('OnWhatsAppConnectSuccess...');

        $params['id'] = 'onconnect';
        $params['code'] = '200';
        $this->PushEvent('onconnectsuccess', $params);
    }

    public function OnWhatsAppConnectError ($phoneNumber, $socket, $error)
    {
        $this->_debug_print('OnWhatsAppConnectError...');

        $params['id'] = 'onconnect';
        $params['error'] = $error;
        $params['code'] = '500';

        $this->PushEvent('onconnecterror', $params);
    }

    public function OnWhatsAppDisconnect ($phoneNumber, $socket)
    {
        $this->_debug_print('OnWhatsAppDisconnect....');
        $this->Cleanup();
    }

    public function OnMessageReceivedServer ($phoneNumber, $from, $id, $class, $t)
    {
        $params ['from'] = WagentProt::ParseID ($from);
        $params ['id'] = $id;
        $params ['class'] = $class;
        $params ['t'] = $t;
        $this->PushEvent('onmessagereceivedserver', $params);
    }

    public function OnMessageReceivedClient ($phoneNumber, $from, $id, $class, $t, $participant = null)
    {
        $params ['from'] = WagentProt::ParseID ($from);
        $params ['id'] = $id;
        $params ['class'] = $class;
        $params ['t'] = $t;
        if (!empty($participant))
            $params ['participant'] = WagentProt::ParseID($participant);
        $this->PushEvent('onmessagereceivedclient', $params);
    }

    public function OnGetPrivacySettings($phoneNumber, $id, $values)
    {
        $params ['id'] = $id;
        $params ['values'] = $values;
        $this->PushEvent('ongetprivacysettings', $params);
    }

    public function OnGetClientConfig($phoneNumber, $id, $platform, $clientId, $lg, $lc, $preview, $default, $groups, $call)
    {
        $params ['id'] = $id;
        $params ['platform'] = $platform;
        $params ['clientid'] = $clientId;
        $params ['lg'] = $lg;
        $params ['lc'] = $lc;
        $params ['preview'] = $preview;
        $params ['default'] = $default;
        $params ['groups'] = $groups;
        $params ['call'] = $call;
        $this->PushEvent('ongetclientconfig', $params);
    }

    public function OnGetMessage ($phoneNumber, $from, $id, $type, $t, $notify, $data)
    {
        $params ['from'] = WagentProt::ParseID ($from);
        $params ['id'] = $id;
        $params ['type'] = $type;
        $params ['t'] = $t;
        $params ['notify'] = $notify;
        $params ['data'] = $data;
        $this->PushEvent('ongetmessage', $params);
    }

    public function OnGetGroupImage ($phoneNumber,
                                     $from,
                                     $participant,
                                     $id,
                                     $type,
                                     $t,
                                     $notify,
                                     $size,
                                     $url,
                                     $file,
                                     $mimetype,
                                     $filehash,
                                     $width,
                                     $height,
                                     $data,
                                     $caption
                                     )
    {
        $params ['from'] = WagentProt::ParseID ($from);
        $params ['participant'] = WagentProt::ParseID($participant);
        $params ['id'] = $id;
        $params ['type'] = $type;
        $params ['t'] = $t;
        $params ['notify'] = $notify;
        $params ['size'] = $size;
        $params ['url'] = $url;
        $params ['file'] = $file;
        $params ['mimetype'] = $mimetype;
        $params ['filehash'] = $filehash;
        $params ['width'] = $width;
        $params ['height'] = $height;
        $params ['data'] = $data;
        $params ['caption'] = $caption;

        $this->PushEvent('ongetgroupimage', $params);
    }

    public function OnGetGroupVideo ($phoneNumber,
                                     $from,
                                     $participant,
                                     $id,
                                     $type,
                                     $t,
                                     $notify,
                                     $url,
                                     $file,
                                     $size,
                                     $mimetype,
                                     $filehash,
                                     $duration,
                                     $vcodec,
                                     $acodec,
                                     $data,
                                     $caption,
                                     $width,
                                     $height,
                                     $fps,
                                     $vbitrate,
                                     $asampfreq,
                                     $asampfmt,
                                     $abitrate
                                     )
    {
        $params ['from'] = WagentProt::ParseID ($from);
        $params ['participant'] = WagentProt::ParseID($participant);
        $params ['id'] = $id;
        $params ['type'] = $type;
        $params ['t'] = $t;
        $params ['notify'] = $notify;
        $params ['url'] = $url;
        $params ['file'] = $file;
        $params ['size'] = $size;
        $params ['mimetype'] = $mimetype;
        $params ['filehash'] = $filehash;
        $params ['duration'] = $duration;
        $params ['vcodec'] = $vcodec;
        $params ['acodec'] = $acodec;
        $params ['data'] = $data;
        $params ['caption'] = $caption;
        $params ['width'] = $width;
        $params ['height'] = $height;
        $params ['fps'] = $fps;
        $params ['vbitrate'] = $vbitrate;
        $params ['asampfreq'] = $asampfreq;
        $params ['asampfmt'] = $asampfmt;
        $params ['abitrate'] = $abitrate;

        $this->PushEvent('ongetgroupvideo', $params);
    }

    public function OnGetGroupMessage ($phoneNumber, $from, $participant, $id, $type, $t, $notify, $data)
    {
        $params ['from'] = WagentProt::ParseID ($from);
        $params ['participant'] = WagentProt::ParseID($participant);
        $params ['id'] = $id;
        $params ['type'] = $type;
        $params ['t'] = $t;
        $params ['notify'] = $notify;
        $params ['data'] = $data;
        $this->PushEvent('ongetgroupmessage', $params);
    }

    public function OnGetImage ($phoneNumber, $from, $id, $type, $t, $notify,
                                $size,
                                $url,
                                $file,
                                $mimetype,
                                $filehash,
                                $width,
                                $height,
                                $data,
                                $caption)
    {
        $params ['from'] = WagentProt::ParseID ($from);
        $params ['id'] = $id;
        $params ['type'] = $type;
        $params ['t'] = $t;
        $params ['notify'] = $notify;
        $params ['size'] = $size;
        $params ['url'] = $url;
        $params ['file'] = $file;
        $params ['mimetype'] = $mimetype;
        $params ['filehash'] = $filehash;
        $params ['width'] = $width;
        $params ['height'] = $height;
        $params ['data'] = $data;
        $params ['caption'] = $caption;
        $this->PushEvent('ongetimage', $params);
    }

    public function OnGetVideo ($phoneNumber, $from, $id, $type, $t, $notify,
                                $url,
                                $file,
                                $size,
                                $mimetype,
                                $filehash,
                                $duration,
                                $vcodec,
                                $acodec,
                                $data,
                                $caption,
                                $width,
                                $height,
                                $fps,
                                $vbitrate,
                                $asampfreq,
                                $asampfmt,
                                $abitrate)
    {
        $params ['from'] = WagentProt::ParseID ($from);
        $params ['id'] = $id;
        $params ['type'] = $type;
        $params ['t'] = $t;
        $params ['notify'] = $notify;
        $params ['size'] = $size;
        $params ['url'] = $url;
        $params ['file'] = $file;
        $params ['mimetype'] = $mimetype;
        $params ['filehash'] = $filehash;
        $params ['duration'] = $duration;
        $params ['vcodec'] = $vcodec;
        $params ['acodec'] = $acodec;
        $params ['data'] = $data;
        $params ['caption'] = $caption;
        $params ['width'] = $width;
        $params ['height'] = $height;
        $params ['fps'] = $fps;
        $params ['vbitrate'] = $vbitrate;
        $params ['asampfreq'] = $asampfreq;
        $params ['asampfmt'] = $asampfmt;
        $params ['abitrate'] = $abitrate;
        $this->PushEvent('ongetvideo', $params);
    }

    public function OnGetAudio ($phoneNumber, $from, $id, $type, $t, $notify,
                                $size,
                                $url,
                                $file,
                                $mimetype,
                                $filehash,
                                $seconds,
                                $acodec,
                                $participant)
    {
        $params ['from'] = WagentProt::ParseID ($from);
        $params ['id'] = $id;
        $params ['type'] = $type;
        $params ['t'] = $t;
        $params ['notify'] = $notify;
        $params ['size'] = $size;
        $params ['url'] = $url;
        $params ['file'] = $file;
        $params ['mimetype'] = $mimetype;
        $params ['filehash'] = $filehash;
        $params ['seconds'] = $seconds;
        $params ['acodec'] = $acodec;
        if (!empty($participant))
            $params ['participant'] = WagentProt::ParseID ($participant);
        $this->PushEvent('ongetaudio', $params);
    }


    public function OnGetGroupAudio ($phoneNumber, $from, $participant, $id, $type, $t, $notify,
                                $size,
                                $url,
                                $file,
                                $mimetype,
                                $filehash,
                                $seconds,
                                $acodec
                                )
    {
        $params ['from'] = WagentProt::ParseID ($from);
        $params ['id'] = $id;
        $params ['type'] = $type;
        $params ['t'] = $t;
        $params ['notify'] = $notify;
        $params ['size'] = $size;
        $params ['url'] = $url;
        $params ['file'] = $file;
        $params ['mimetype'] = $mimetype;
        $params ['filehash'] = $filehash;
        $params ['seconds'] = $seconds;
        $params ['acodec'] = $acodec;
        if (!empty($participant))
            $params ['participant'] = WagentProt::ParseID ($participant);
        $this->PushEvent('ongetgroupaudio', $params);
    }



    public function OnGetVCard ($phoneNumber, $from, $id, $type, $t, $notify,
                                $name,
                                $data, $participant)
    {
        $params ['from'] = WagentProt::ParseID ($from);
        $params ['id'] = $id;
        $params ['type'] = $type;
        $params ['t'] = $t;
        $params ['notify'] = $notify;
        $params ['name'] = $name;
        $params ['data'] = $data;
        if (!empty($participant))
            $params ['participant'] = WagentProt::ParseID($participant);
        $this->PushEvent('ongetvcard', $params);
    }

    public function OnGetGroupVCard ($phoneNumber, $from, $participant, $id, $type, $t, $notify,
                                $name,
                                $data)
    {
        $params ['from'] = WagentProt::ParseID ($from);
        $params ['id'] = $id;
        $params ['type'] = $type;
        $params ['t'] = $t;
        $params ['notify'] = $notify;
        $params ['name'] = $name;
        $params ['data'] = $data;
        if (!empty($participant))
            $params ['participant'] = WagentProt::ParseID($participant);
        $this->PushEvent('ongetgroupvcard', $params);
    }

    public function OnGetLocation ($phoneNumber, $from, $id, $type, $t, $notify,
                                $name,
                                $longitude,
                                $latitude,
                                $url,
                                $data, $participant)
    {
        $params ['from'] = WagentProt::ParseID ($from);
        $params ['id'] = $id;
        $params ['type'] = $type;
        $params ['t'] = $t;
        $params ['notify'] = $notify;
        $params ['name'] = $name;
        $params ['longitude'] = $longitude;
        $params ['latitude'] = $latitude;
        $params ['url'] = $url;
        $params ['data'] = $data;
        if (!empty($participant))
            $params ['participant'] = WagentProt::ParseID($participant);
        $this->PushEvent('ongetlocation', $params);
    }

    public function OnGetGroupLocation ($phoneNumber, $from, $participant, $id, $type, $t, $notify,
                                   $name,
                                   $longitude,
                                   $latitude,
                                   $url,
                                   $data)
    {
        $params ['from'] = WagentProt::ParseID ($from);
        $params ['id'] = $id;
        $params ['type'] = $type;
        $params ['t'] = $t;
        $params ['notify'] = $notify;
        $params ['name'] = $name;
        $params ['longitude'] = $longitude;
        $params ['latitude'] = $latitude;
        $params ['url'] = $url;
        $params ['data'] = $data;
        if (!empty($participant))
            $params ['participant'] = WagentProt::ParseID($participant);
        $this->PushEvent('ongetgrouplocation', $params);
    }

    public function OnGroupsParticipantAdd ($phoneNumber, $groupId, $id)
    {
        $params ['groupid'] = WagentProt::ParseID ($groupId);
        $params ['id'] = $id;
        $this->PushEvent('ongroupsparticipantadd', $params);
    }

    public function OnGroupsParticipantChangedNumber($phoneNumber, $groupId, $time, $oldNumber, $notify, $newNumber) 
    {
        $params ['groupid'] = WagentProt::ParseID ($groupId);
        $params ['time'] = $time;
        $params ['oldnumber'] = $oldNumber;
        $params ['notify'] = $notify;
        $params ['newnumber'] = $newNumber;
        $this->PushEvent('ongroupsparticipantchangednumber', $params);
    }

    public function OnParticipantPromote($phoneNumber, $id, $groupId, $participant) 
    {
        $params ['id'] = $id;
        $params ['groupid'] = WagentProt::ParseID ($groupId);
        $params ['participant'] = $this->ParseID ($participant);
        $this->PushEvent('onparticipantpromote', $params);
    }

    public function OnSetPicture($phoneNumber, $id)
    {
        $params ['id'] = $id;
        $this->PushEvent('onsetpicture', $params);
    }

    public function OnStatusUpdate($phoneNumber, $id)
    {
        $params ['id'] = $id;
        $this->PushEvent('onstatusupdate', $params);
    }

    public function OnParticipantDemote($phoneNumber, $id, $groupId, $participant) 
    {
        $params ['id'] = $id;
        $params ['groupid'] = WagentProt::ParseID ($groupId);
        $params ['participant'] = $this->ParseID ($participant);
        $this->PushEvent('onparticipantdemote', $params);
    }

    public function OnGroupsParticipantRemove ($phoneNumber, $groupId, $id)
    {
        $params ['groupid'] = WagentProt::ParseID ($groupId);
        $params ['id'] = $id;
        $this->PushEvent('ongroupsparticipantremove', $params);
    }

    public function OnParticipantAdded($phoneNumber, $groupId, $jid, $id) 
    {
        $params ['groupid'] = WagentProt::ParseID ($groupId);
        $params ['jid'] = WagentProt::ParseID ($jid);
        $params ['id'] = $id;
        $this->PushEvent('onparticipantadded', $params);
    }

    public function OnParticipantRemoved($phoneNumber, $groupId, $jid, $id) 
    {
        $params ['groupid'] = WagentProt::ParseID ($groupId);
        $params ['jid'] = WagentProt::ParseID ($jid);
        $params ['id'] = $id;
        $this->PushEvent('onparticipantremoved', $params);
    }

    public function OnMessageComposing ($phoneNumber, $from, $id, $status, $t)
    {
        $params ['from'] = WagentProt::ParseID ($from);
        $params ['id'] = $id;
        $params ['status'] = $status;
        $params ['t'] = $t;
        $this->PushEvent('onmessagecomposing', $params);
    }

    public function OnMessagePaused ($phoneNumber, $from, $id, $status, $t)
    {
        $params ['from'] = WagentProt::ParseID ($from);
        $params ['id'] = $id;
        $params ['status'] = $status;
        $params ['t'] = $t;
        $this->PushEvent('onmessagepaused', $params);
    }

    public function OnGroupMessageComposing($phoneNumber, $from_group_jid, $from_user_jid, $id, $type, $time)
    {
        $params ['from'] = WagentProt::ParseID ($from_group_jid);
        $params ['participant'] = WagentProt::ParseID ($from_user_jid);
        $params ['id'] = $id;
        $params ['type'] = $type;
        $params ['t'] = $time;
        $this->PushEvent('ongroupmessagecomposing', $params);
    }

    public function OnGroupMessagePaused($phoneNumber, $from_group_jid, $from_user_jid, $id, $type, $t)
    {
        $params ['from'] = WagentProt::ParseID ($from_group_jid);
        $params ['participant'] = WagentProt::ParseID ($from_user_jid);
        $params ['id'] = $id;
        $params ['type'] = $type;
        $params ['t'] = $t;
        $this->PushEvent('ongroupmessagepaused', $params);
    }

    public function OnGetSyncResult ($result, $id)
    {
        $result->existing = $this->ParseID($result->existing);
        $result->nonExisting = $this->ParseID($result->nonExisting);

        $params ['result'] = $result;
        $params ['id'] = $id;
        $this->PushEvent('ongetsyncresult', $params);
    }

    public function OnGetReceipt ($from, $id, $offline, $retry, $participant)
    {
        $params ['from'] = WagentProt::ParseID ($from);
        $params ['id'] = $id;
        $params ['offline'] = $offline;
        $params ['retry'] = $retry;
        if (!empty($participant))
            $params ['participant'] = WagentProt::ParseID($participant);
        $this->PushEvent('ongetreceipt', $params);
    }

    public function OnGetPrivacyBlockedList ($phoneNumber, $id, $result)
    {
        $params ['result'] = $this->ParseID($result);
        $params ['id'] = $id;
        $this->PushEvent('ongetprivacyblockedlist', $params);
    }

    public function OnGetServerProperties ($phoneNumber, $id, $version, $props)
    {
        $params ['id'] = $id;
        $params ['version'] = $version;
        $params ['props'] = $props;
        $this->PushEvent('ongetserverproperties', $params);
    }

    public function OnGroupsChatCreate ($phoneNumber, $groupId, $id)
    {
        $params ['groupid'] = WagentProt::ParseID ($groupId);
        $params ['id'] = $id;
        $this->PushEvent('ongroupschatcreate', $params);
    }

    public function OnGroupsSubjectSet ($phoneNumber, $groupId, $id)
    {
        $params ['groupid'] = WagentProt::ParseID ($groupId);
        $params ['id'] = $id;
        $this->PushEvent('ongroupssubjectset', $params);
    }

    public function OnGroupsChatEnd ($phoneNumber, $groupId,  $id)
    {
        $params ['groupid'] = $groupId;
        $params ['id'] = $id;
        $this->PushEvent('ongroupschatend', $params);
    }

    public function OnGetGroups ($phoneNumber, $id, $groupList)
    {
        $params ['id'] = $id;
        foreach ($groupList as $key => $group) {
            $groupList [$key] ['creator'] = $this->ParseID ($group ['creator']);
            $groupList [$key] ['s_o'] = $this->ParseID ($group ['s_o']);
        }
        $params ['grouplist'] = $groupList;
        $this->PushEvent('ongetgroups', $params);
    }

    public function OnGetGroupV2Info ($phoneNumber,
                $groupID,
                $creator,
                $creation,
                $subject,
                $participants,
                $admins,
                $fromGetGroups, $msgid)
    {
        $info ['groupid'] = $groupID;
        $info ['creator'] = $creator;
        $info ['creation'] = $creation;
        $info ['subject'] = $subject;
        $info ['participants'] = $this->ParseID($participants);
        $info ['admins'] = $this->ParseID($admins);

        if (!$fromGetGroups || $msgid == null) {
            $this->PushEvent('ongetgroupv2info', $info);
            return;
        }

        $index = $this->GetEventIndex ($msgid);
        if ($index == -1) {
            $this->PushEvent('ongetgroupv2info', $info);
            return;
        }

        $this->UpdateGroupEventParticipants ($index, $groupID, $info ['participants'], $info ['admins']);
    }

    function UpdateGroupEventParticipants ($index, $groupID, $participants, $admins)
    {
        $event = $this->GetEventFromIndex ($index);

        if ($event == null)
            return;

        $data = $event ['data'];

        if(!isset($data['grouplist']))
            return;

        $groupList = $data['grouplist'];

        foreach ($groupList as $key => $group) {
            if ($groupList [$key] ['id'] != $groupID)
                continue;
            $groupList [$key] ['participants'] = $participants;
            $groupList [$key] ['admins'] = $admins;
        }

        $data ['grouplist'] = $groupList;
        $event ['data'] = $data;

        $this->ReplaceEventAtIndex ($index, $event);
    }

    public function OnGetStatuses ($phoneNumber, $id, $statuses)
    {
        $params ['id'] = $id;

        $result = [];

        // Cleanup all from values with only the phonenumber.
        foreach ($statuses as $key => $value) {
            $status['contact_id']   = $this->ParseID($value ['from']);
            $status['status_message'] = $value ['data'];
            $result[] = $status;
        }

        $params ['statuses_messages'] = $result;

        $this->PushEvent('ongetstatuses', $params);
    }

    public function OnGetStatus ($phoneNumber, $from, $status, $id, $t, $data)
    {
        $params ['from'] = WagentProt::ParseID ($from);
        $params ['status'] = $status;
        $params ['id'] = $id;
        $params ['t'] = $t;
        $params ['data'] = $data;
        $this->PushEvent('ongetstatus', $params);
    }

    public function OnGetError ($phoneNumber, $from, $id, $tag, $type)
    {
        $code = $tag->getAttribute ('code');
        $text = $tag->getAttribute ('text');

        $params ['from'] = WagentProt::ParseID ($from);
        $params ['id'] = $id;
        if (empty($code))
            $params ['code'] = '';
        else
            $params ['code'] = $code;
        if (empty($text))
            $params ['text'] = '';
        else
            $params ['text'] = $text;
        $params ['type'] = $type;
        $this->PushEvent('ongeterror', $params);
    }

    public function OnStreamError ($tag)
    {
        $this->_debug_print('OnStreamError...');

        $text = $tag->getAttribute ('text');
        if (empty($text))
            $params ['text'] = 'Stream Error: ' . $tag->getTag();
        else
            $params ['text'] = 'Stream Error: ' . $text;
        $params ['code'] = '500';

        $this->PushEvent('onstreamerror', $params);

        $this->Cleanup();
    }

    public function OnProfilePictureChanged ($phoneNumber, $from, $id, $t)
    {
        $params ['from'] = WagentProt::ParseID ($from);
        $params ['id'] = $id;
        $params ['t'] = $t;
        $this->PushEvent('onprofilepicturechanged', $params);
    }

    public function OnProfilePictureDeleted ($phoneNumber, $from, $id, $t)
    {
        $params ['from'] = WagentProt::ParseID ($from);
        $params ['id'] = $id;
        $params ['t'] = $t;
        $this->PushEvent('onprofilepicturedeleted', $params);
    }

    public function OnMediaUploadFailed ($phoneNumber, $id, $node, $messageNode, $text)
    {
        $params ['id'] = $id;
        $params ['code'] = '400';
        $params ['text'] = $text;
        $this->PushEvent('onmediauploadfailed', $params);
    }

    public function OnMediaMessageSent ($phoneNumber, $to,
                $id,
                $filetype,
                $url,
                $filename,
                $filesize,
                $filehash,
                $caption,
                $icon)
    {
        $params ['filetype'] = $filetype;
        $params ['to'] = $to;
        $params ['id'] = $id;
        $params ['url'] = $url;
        $params ['filename'] = $filename;
        $params ['filehash'] = $filehash;
        $params ['filesize'] = $filesize;
        $params ['caption'] = $caption;
        $this->PushEvent('onmediamessagesent', $params);
    }

    public function OnClose ($phoneNumber, $error)
    {
        $this->_debug_print('OnClose...');
        $this->Cleanup();
    }

    function BindRegistrationEvents ()
    {
        $this->registration->eventManager()->bind('onCredentialsBad', [$this, 'OnCredentialsBad']);
        $this->registration->eventManager()->bind('onCodeRegisterFailed', [$this, 'OnCodeRegisterFailed']);
        $this->registration->eventManager()->bind('onCredentialsGood', [$this, 'OnCredentialsGood']);
        $this->registration->eventManager()->bind('onCodeRegister', [$this, 'OnCodeRegister']);
        $this->registration->eventManager()->bind('onCodeRequestFailedTooRecent', [$this, 'OnCodeRequestFailedTooRecent']);
        $this->registration->eventManager()->bind('onCodeRequestFailedTooManyGuesses', [$this, 'OnCodeRequestFailedTooManyGuesses']);
        $this->registration->eventManager()->bind('onCodeRequest', [$this, 'OnCodeRequest']);
        $this->registration->eventManager()->bind('onCodeRequestFailed', [$this, 'OnCodeRequestFailed']);
    }

    function BindEvents ()
    {
        $this->wa->eventManager()->bind('onPresenceAvailable', [$this, 'OnPresenceAvailableReceived']);
        $this->wa->eventManager()->bind('onPresenceUnavailable', [$this, 'OnPresenceUnavailableReceived']);
        $this->wa->eventManager()->bind('onConnect', [$this, 'OnWhatsAppConnectSuccess']);
        $this->wa->eventManager()->bind('onConnectError', [$this, 'OnWhatsAppConnectError']);
        $this->wa->eventManager()->bind('onDisconnect', [$this, 'OnWhatsAppDisconnect']);
        $this->wa->eventManager()->bind('onMessageComposing', [$this, 'OnMessageComposing']);
        $this->wa->eventManager()->bind('onMessagePaused', [$this, 'OnMessagePaused']);
        $this->wa->eventManager()->bind('onGroupMessageComposing', [$this, 'OnGroupMessageComposing']);
        $this->wa->eventManager()->bind('onGroupMessagePaused', [$this, 'OnGroupMessagePaused']);
        $this->wa->eventManager()->bind('onGetImage', [$this, 'OnGetImage']);
        $this->wa->eventManager()->bind('onGetVideo', [$this, 'OnGetVideo']);
        $this->wa->eventManager()->bind('onGetAudio', [$this, 'OnGetAudio']);
        $this->wa->eventManager()->bind('onGetGroupAudio', [$this, 'OnGetGroupAudio']);
        $this->wa->eventManager()->bind('onGetvCard', [$this, 'OnGetvCard']);
        $this->wa->eventManager()->bind('onGetGroupvCard', [$this, 'OnGetGroupvCard']);
        $this->wa->eventManager()->bind('onGetSyncResult', [$this, 'OnGetSyncResult']);
        $this->wa->eventManager()->bind('onGetReceipt', [$this, 'OnGetReceipt']);
        $this->wa->eventManager()->bind('onGetPrivacyBlockedList', [$this, 'OnGetPrivacyBlockedList']);
        $this->wa->eventManager()->bind('onGetServerProperties', [$this, 'OnGetServerProperties']);
        $this->wa->eventManager()->bind('onGetProfilePicture', [$this, 'OnGetProfilePicture']);
        $this->wa->eventManager()->bind('onGroupsChatCreate', [$this, 'OnGroupsChatCreate']);
        $this->wa->eventManager()->bind('onGroupsSubjectSet', [$this, 'OnGroupsSubjectSet']);
        $this->wa->eventManager()->bind('onGetGroups', [$this, 'OnGetGroups']);
        $this->wa->eventManager()->bind('onGroupsChatEnd', [$this, 'OnGroupsChatEnd']);
        $this->wa->eventManager()->bind('onGetGroupV2Info', [$this, 'OnGetGroupV2Info']);
        $this->wa->eventManager()->bind('onGetStatus', [$this, 'OnGetStatus']);
        $this->wa->eventManager()->bind('onGetStatuses', [$this, 'OnGetStatuses']);
        $this->wa->eventManager()->bind('onGetError', [$this, 'OnGetError']);
        $this->wa->eventManager()->bind('onStreamError', [$this, 'OnStreamError']);
        $this->wa->eventManager()->bind('onProfilePictureChanged', [$this, 'OnProfilePictureChanged']);
        $this->wa->eventManager()->bind('onProfilePictureDeleted', [$this, 'OnProfilePictureDeleted']);
        $this->wa->eventManager()->bind('onParticipantsPromote', [$this, 'OnParticipantPromote']);
        $this->wa->eventManager()->bind('onParticipantsDemote', [$this, 'OnParticipantDemote']);
        $this->wa->eventManager()->bind('onSetPicture', [$this, 'OnSetPicture']);
        $this->wa->eventManager()->bind('onStatusUpdate', [$this, 'OnStatusUpdate']);
        $this->wa->eventManager()->bind('onGroupsParticipantsRemove', [$this, 'OnGroupsParticipantRemove']);
        $this->wa->eventManager()->bind('onGroupsParticipantsAdd', [$this, 'OnGroupsParticipantAdd']);
        $this->wa->eventManager()->bind('onParticipantAdded', [$this, 'OnParticipantAdded']);
        $this->wa->eventManager()->bind('onParticipantRemoved', [$this, 'OnParticipantRemoved']);
        $this->wa->eventManager()->bind('onGroupsParticipantChangedNumber', [$this, 'OnGroupsParticipantChangedNumber']);
        $this->wa->eventManager()->bind('onMediaUploadFailed', [$this, 'OnMediaUploadFailed']);
        $this->wa->eventManager()->bind('onMediaMessageSent', [$this, 'OnMediaMessageSent']);
        $this->wa->eventManager()->bind('onClose', [$this, 'OnClose']);
        $this->wa->eventManager()->bind('onMessageReceivedServer', [$this, 'OnMessageReceivedServer']);
        $this->wa->eventManager()->bind('onMessageReceivedClient', [$this, 'OnMessageReceivedClient']);
        $this->wa->eventManager()->bind('onGetClientConfig', [$this, 'OnGetClientConfig']);
        $this->wa->eventManager()->bind('onGetPrivacySettings', [$this, 'OnGetPrivacySettings']);
        $this->wa->eventManager()->bind('onGetMessage', [$this, 'OnGetMessage']);
        $this->wa->eventManager()->bind('onGetLocation', [$this, 'OnGetLocation']);
        $this->wa->eventManager()->bind('onGetGroupLocation', [$this, 'OnGetGroupLocation']);
        $this->wa->eventManager()->bind('onGetGroupMessage', [$this, 'OnGetGroupMessage']);
        $this->wa->eventManager()->bind('onGetGroupImage', [$this, 'OnGetGroupImage']);
        $this->wa->eventManager()->bind('onGetGroupVideo', [$this, 'OnGetGroupVideo']);
    }

    public function GetPicturesFolder ()
    {
        $picturesFolder = getcwd() . DIRECTORY_SEPARATOR . Constants::DATA_FOLDER . DIRECTORY_SEPARATOR . Constants::PICTURES_FOLDER;
        return $picturesFolder;
    }

    private function GetProfilePicturePath ($type, $from)
    {
        if ($type == 'preview')
            return $this->GetPicturesFolder (). DIRECTORY_SEPARATOR . $from . '.preview.jpg';
        return $this->GetPicturesFolder () . DIRECTORY_SEPARATOR. $from . '.jpg';
    }

    public function OnGetProfilePicture($phoneNumber, $id, $from, $type, $data)
    {
        $from = WagentProt::ParseID ($from);
        $filename = $this->GetProfilePicturePath ($type, $from);
        
        $fp = @fopen($filename, 'w');
        if ($fp) {
            fwrite($fp, $data);
            fclose($fp);
        }
        $params ['id'] = $id;
        $params ['from'] = $from;
        $params ['type'] = $type;
        $params ['filename'] = $filename;
        $this->PushEvent('ongetprofilepicture', $params);
    }

    function UpdatePresenceEvent ($index, $connected_status, $contact_id)
    {
        $event = $this->GetEventFromIndex ($index);

        if ($event == null)
            return;

        $params = $event ['data'];
        $params ['connected_status'][$contact_id] = $connected_status;

        $event ['data'] = $params;

        $this->ReplaceEventAtIndex ($index, $event);
    }

    public function OnPresenceAvailableReceived($phoneNumber, $from)
    {
        $contact_id = WagentProt::ParseID($from);
        $connected_status =  'online';

        $params ['id'] = 'onpresence';
        $params ['connected_status'][$contact_id] = $connected_status;

        $index = $this->GetEventIndex ('onpresence');

        if ($index == -1) {
            $this->PushEvent('onpresence', $params);
            return;
        }

        $this->UpdatePresenceEvent ($index, $connected_status, $contact_id);
    }

    public function OnPresenceUnavailableReceived($phoneNumber, $from, $last)
    {
        $contact_id = WagentProt::ParseID($from);
        $connected_status = $last;

        $params ['id'] = 'onpresence';
        $params ['connected_status'][$contact_id] = $connected_status;

        $index = $this->GetEventIndex ('onpresence');

        if ($index == -1) {
            $this->PushEvent('onpresence', $params);
            return;
        }

        $this->UpdatePresenceEvent ($index, $connected_status, $contact_id);
    }

    public function __construct($ip = null, $timeout = 30, $debug = false)
    {
        $this->idleTimeout = $timeout;
        $this->debug = $debug;

        $socketTimeout = null;
        if ($timeout > 5)
            $socketTimeout = $timeout / 5;

        parent::__construct($ip, 0, $socketTimeout);

        $this->masterSocket->setBlocking(true);

        $this->addHook(Server::HOOK_CONNECT, [$this, 'OnConnect']);
        $this->addHook(Server::HOOK_INPUT, [$this, 'OnInput']);
        $this->addHook(Server::HOOK_DISCONNECT, [$this, 'OnDisconnect']);
        $this->addHook(Server::HOOK_TIMEOUT, [$this, 'OnTimeout']);
        $this->readType = PHP_NORMAL_READ;
        $this->ResetIdleTimer ();
    }

    public function OnConnect(Server $server, Socket $client, $message)
    {
        $this->_debug_print('OnConnect...');
        $this->_debug_print($message);
    }

    public function Start ()
    {
        $this->_debug_print('Start...');

        $this->run ();
    }

    function ResetIdleTimer ()
    {
        $this->timeStart = microtime(true);
    }

    function ForceServerQuit ()
    {
        $this->timeStart = 0;
    }

    function IdleTime ()
    {
        return microtime(true) - $this->timeStart;
    }

    public function OnTimeout(Server $server, Socket $client)
    {
        $this->SafePollMessage ();

        $idleTime = $this->IdleTime ();

        if ($idleTime > $this->idleTimeout) {
          $this->Cleanup();
          return Server::RETURN_HALT_SERVER;
        }
    }

    /**
     * Overrideable Read Functionality
     * @param Socket $client
     * @return string
     */
    protected function read(Socket $client)
    {
        try {
          return parent::read ($client);
        }
        catch (SocketException $e)
        {
            $this->_debug_print('Exception reading socket');
            $this->_debug_print($e);
        	return '';
        }
    }

    public function OnInput(Server $server, Socket $client, $message)
    {
        $this->_debug_print('OnInput...');
        $this->_debug_print($client);
        $this->_debug_print($message);

        $message = trim ($message);
        if (empty ($message))
            return;
        try {

          $this->ResetIdleTimer ();
          $quit = $this->HandleMessage($client, $message);

          if ($quit) {
              $this->Cleanup();
              return Server::RETURN_HALT_SERVER;
          }
        }
        catch (Exception $e)
        {
          // Something went wrong...just close the our current connecton
          $this->_debug_print('[Exception] OnInput ------- ');
          $this->_debug_print($e);
          $this->Cleanup();
        }
    }

    private function IsSocketWritable ()
    {
        $r = [];
        $w = [$this->wa->getSocket()];
        $e = [];
        $s = socket_select($r, $w, $e, 0, 10);
        return $s != 0;
    }

    private function CreateRegistration ()
    {
        $this->_debug_print ('CreateRegistration....');

        $this->registration = new WagentRegistration($this->number);
        if ($this->eventQueue == null)
            $this->eventQueue = new SplQueue();
        $this->BindRegistrationEvents();
    }

    function IsRegistrationInitialized ()
    {
        if (!isset ($this->registration) || $this->registration == null)
            return false;
        return true;
    }

    function IsLiteConnected ()
    {
        if ($this->IsRegistrationInitialized ())
            return true;
        if (!empty($this->number))
            return true;
        return false;
    }

    function IsInitialized ()
    {
        if (!isset($this->wa) || $this->wa == null)
            return false;
        return true;
    }


    function IsConnected ()
    {
      if (!isset($this->wa) || $this->wa == null)
          return false;
      if (!$this->wa->isConnected())
          return false;
      if(!is_resource($this->wa->getSocket ()))
          return false;
      return $this->IsSocketWritable ();
    }    

    function IsLoggedIn ()
    {
      if (!$this->IsConnected())
        return false;
      return $this->wa->isLoggedIn();
    }

    function Cleanup ()
    {
        $this->_debug_print ('Cleanup....');

        if (!isset($this->wa) || $this->wa == null || $this->isCleaningUp)
            return;
        $this->isCleaningUp = true;
        $this->isActive = false;

        $this->SavePendingEvents ();

        $this->wa->disconnect ();
        $this->wa = null;
        unset($this->wa);

        unset ($this->eventQueue);
        $this->eventQueue = null;
        $this->isCleaningUp = false;
    }

    private function GetEventsFile ()
    {
        $eventsFile = getcwd() . DIRECTORY_SEPARATOR . Constants::DATA_FOLDER . DIRECTORY_SEPARATOR . AgentServer::PENDIND_EVENTS_FILE;
        return $eventsFile;
    }

    private function RestorePendingEvents ()
    {
        $eventsFile = $this->GetEventsFile ();
        if (!file_exists($eventsFile))
            return;
        $data = file_get_contents($eventsFile);
        unlink($eventsFile);
        if (empty($data))
            return;
        $this->eventQueue->unserialize($data);
    }

    private function RemoveStreamErrorEvents ()
    {
        if ($this->eventQueue->isEmpty())
            return;

        $indexesToRemove = [];

        $this->eventQueue->rewind();

        while ($this->eventQueue->valid()) {

            $event = $this->eventQueue->current();
            $eventName  = $event ['name'];

            if ($eventName == 'onstreamerror')
                $indexesToRemove [] = $this->eventQueue->key();

            $this->eventQueue->next();
        }

        foreach (array_reverse($indexesToRemove) as $index)
            $this->eventQueue->offsetUnset($index);

        $this->eventQueue->rewind();
    }

    private function SavePendingEvents ()
    {
        $eventsFile = $this->GetEventsFile ();

        $this->RemoveStreamErrorEvents();

        if (empty($this->eventQueue) || $this->eventQueue->isEmpty())
            return;

        $data = $this->eventQueue->serialize();
        file_put_contents($eventsFile, $data);
    }

    public function OnDisconnect(Server $server, Socket $client, $message)
    {

    }

    function SafePollMessage ($forcePeek = false)
    {
      if (!$this->IsConnected ())
          return;
      $this->PollMessages ($forcePeek);
    }

    function PollMessages ($forcePeek = false)
    {
        if (!$this->IsConnected ())
            return;
        //
        //  HACK: This call is here due pollMessage bug,
        //  calling pollMessage not necessarily bring all events, we need to send something to the server to receive
        //  pending events
        $polledEvents = 0;

        $this->everPolledMessages = true;
        for ($i = 0; $i < 1000; $i++) {
                if (!$this->IsConnected ())
                    break;
                if($this->wa->pollMessage(200))
                    $polledEvents ++;
            usleep(50);
        }
        // HACK if pollMessage failed to fetch any new messages, send a getGroups node to force
        // server to puke the events
        if ($polledEvents < 5 && $forcePeek == true) {

            if ($this->forcedEventFlushed) {
                // HACK2: We need to poke the message server to receive any update
                // We do this by sending a message for ourselves
                $this->wa->sendMessage($this->number, 'PING');
                $this->forcedEventFlushed = false;
            }

            for ($i = 0; $i < 1000; $i++) {
                if (!$this->IsConnected ())
                    break;
                $this->wa->pollMessage(200);
                usleep(50);
            }
        }
    }

    function ReadArray (Socket $client)
    {
        $array = $this->ReadLine ($client);
        if ($array == null)
            return null;
        return explode ('|', $array);
    }

    function ReadInt (Socket $client)
    {
        $line = $this->ReadLine ($client);
        if (empty($line))
            return 0;
        return intval($line);
    }

    function ReadBool (Socket $client)
    {
        $line = $this->ReadLine ($client);
        if (empty($line))
            return false;
        return strcasecmp($line, 'false') != 0;
    }

    private function ReadSocketLine (Socket $client)
    {
        $this->_debug_print('ReadSocketLine...');
        $buff = $client->read (AgentServer::MAXREAD_LINE, PHP_NORMAL_READ);
        $this->_debug_print($buff);

        $len = strlen ($buff);
        $line = $buff;

        if ($len <= 0)
            return $line;

        while ($buff [$len - 1] != "\n") {

            $buff = $client->read (AgentServer::MAXREAD_LINE, PHP_NORMAL_READ);
            $len = strlen ($buff);

            if ($len <= 0)
                return $line;

            $line .= $buff;
        }
        return $line;
    }

    function ReadLine (Socket $client)
    {
        // There is a good reason why the ReadLine is written like this:
        // TELNET send extra \n and empty spaces 
        // So to keep easy to test the server from Python or from Telnet we ignore the extra empty spaces
        // To send empty string we send a fake 'empty-token'

        do {
            $read = $this->ReadSocketLine ($client);
            $line   = trim($read);
        } while ($line !== '0' && empty ($line));

        $value = str_replace("\\n", "\n", $line);
        if ($value == '_none_a35825979c956e5a1f068e7cb21c280c')
            return null;
        return $value;
    }

    function WriteLine (Socket $client, $data)
    {
        $this->_debug_print('WriteLine...');
        $this->_debug_print($data);

        if ($data == null || $data == '')
            $line = '_none_a35825979c956e5a1f068e7cb21c280c';
        else
            $line = str_replace("\n", "\\n", $data);
        $client->send ($line . "\r\n");
    }

    function WriteObject (Socket $client, $data)
    {
        if (empty($data))
            $data_str = '{}';
        else
            $data_str = json_encode($data);
        $this->WriteLine ($client, $data_str);
    }

    function HandleMessage(Socket $client, $message)
    {
        try {
            $this->_HandleMessage($client, $message);
        } catch (Exception $e) {

            if ($message == 'login') {
                $this->WriteLine($client, 'ERROR');
            } else if ($message == 'peekeventsforce' || $message == 'peekevents') {
                $this->WriteLine($client, 'onerror');
                $result['error'] = 'Error handling ('.$message.') Message: ' . $e->getMessage() . ' ('. get_class($e) .')';
                $result['code'] = '500';
                $this->WriteObject ($client, $result);
                $this->WriteLine($client, 'ERROR');
            } else {
                $result['error'] = 'Error handling ('.$message.') Message: ' . $e->getMessage(). ' ('. get_class($e) .')';
                $result['code'] = '500';
                $this->WriteObject ($client, $result);
            }
            throw $e;
        }
    }

    function _HandleMessage (Socket $client, $message)
    {
        switch ($message) {
            case 'isliteconnected':
                $isliteconnected = $this->IsLiteConnected();
                if ($isliteconnected)
                  $this->WriteLine ($client, '1');
                else
                  $this->WriteLine ($client, '0');
                break;
            case 'isconnected':
                $isconnected = $this->IsConnected ();
                if ($isconnected)
                  $this->WriteLine ($client, '1');
                else
                  $this->WriteLine ($client, '0');
                break;
            case 'isloggedin':
                $isloggedin = $this->IsLoggedIn ();
                if ($isloggedin)
                  $this->WriteLine ($client, '1');
                else
                  $this->WriteLine ($client, '0');
                break;
            case 'liteconnect':
                $number = $this->ReadLine($client);
                $result = $this->LiteConnect ($number);
                $this->WriteObject($client, $result);
                break;
            case 'connect':
                $number  = $this->ReadLine($client);
                $nickname = $this->ReadLine($client);
                $autoReply = $this->ReadInt($client);

                $result = $this->Connect($number, $nickname, $autoReply);
                $this->WriteObject ($client, $result);
                break;
            case 'login':
                $password = $this->ReadLine($client);
                $ok = $this->Login ($password);
                if (!$ok)
                    $this->WriteLine ($client, 'ERROR');
                else
                    $this->WriteLine ($client, 'OK');
                break;
            case 'disconnect':
                $this->Close ();
                break;
            case 'sendactivestatus':
                $this->SendActiveStatus ();
                $this->WriteLine ($client, 'OK');
                break;
            case 'sendofflinestatus':
                $this->SendOfflineStatus();
                $this->WriteLine ($client, 'OK');
                break;
            case 'getconnectedstatus':
                $connected_status = $this->GetConnectedStatus();
                $result['connected_status'] = $connected_status;
                $result['code'] = '200';
                $this->WriteObject ($client, $result);
                break;
            case 'sendgetgroups':
                $result = $this->SendGetGroups ();
                $this->WriteObject ($client, $result);
                break;
            case 'sendchangenumber':
                $number = $this->ReadLine($client);
                $result = $this->SendChangeNumber ($number);
                $this->WriteObject ($client, $result);
                break;
            case 'sendgetclientconfig':
                $result = $this->SendGetClientConfig ();
                $this->WriteObject ($client, $result);
                break;
            case 'sendgetgroupv2info':
                $groupId = $this->ReadLine($client);
                $this->SendGetGroupV2Info ($groupId);
                $this->WriteLine ($client, 'OK');
                break;
            case 'peekevents':
                $this->PeekEvents ($client);
                $this->WriteLine ($client, 'OK');
                break;
            case 'peekeventsforce':
                $this->PeekEvents ($client, true);
                $this->WriteLine ($client, 'OK');
                break;
            case 'sendsetprivacysettings':
                $category = $this->ReadLine($client);
                $value  = $this->ReadLine($client);
                $result = $this->SendSetPrivacySettings($category, $value);
                $this->WriteObject ($client, $result);
                break;
            case 'sendgetprivacysettings':
                $result = $this->SendGetPrivacySettings();
                $this->WriteObject ($client, $result);
                break;
            case 'sendgetprofilepicture':
                $number = $this->ReadLine($client);
                $type = $this->ReadLine($client);
                $result = $this->SendGetProfilePicture($number, $type);
                $this->WriteObject ($client, $result);
                break;
            case 'sendgetserverproperties':
                $result = $this->SendGetServerProperties();
                $this->WriteObject ($client, $result);
                break;
            case 'sendextendaccount':
                $this->SendExtendAccount();
                $this->WriteLine ($client, 'OK');
                break;
            case 'sendremoveaccount':
                $lg = $this->ReadLine($client);
                $lc = $this->ReadLine($client);
                $feedback = $this->ReadLine($client);
                $result = $this->SendRemoveAccount($lg, $lc, $feedback);
                $this->WriteObject ($client, $result);
                break;
            case 'sendgetstatuses':
                $jids = $this->ReadArray($client);
                $result = $this->SendGetStatuses($jids);
                $this->WriteObject ($client, $result);
                break;
            case 'sendgroupschatcreate':
                $subject = $this->ReadLine($client);
                $participants = $this->ReadArray($client);
                $result = $this->SendGroupsChatCreate($subject, $participants);
                $this->WriteObject ($client, $result);
                break;
            case 'sendsetgroupsubject':
                $gjid = $this->ReadLine($client);
                $subject = $this->ReadLine($client);
                $result = $this->SendSetGroupSubject($gjid, $subject);
                $this->WriteObject ($client, $result);
                break;
            case 'sendgroupsleave':
                $gjid = $this->ReadLine($client);
                $result = $this->SendGroupsLeave($gjid);
                $this->WriteObject ($client, $result);
                break;
            case 'sendgroupsparticipantadd':
                $gjid = $this->ReadLine($client);
                $participant = $this->ReadLine($client);
                $result = $this->SendGroupsParticipantAdd($gjid, $participant);
                $this->WriteObject ($client, $result);
                break;
            case 'sendgroupsparticipantremove':
                $gjid = $this->ReadLine($client);
                $participant = $this->ReadLine($client);
                $result = $this->SendGroupsParticipantRemove($gjid, $participant);
                $this->WriteObject ($client, $result);
                break;
            case 'sendpromoteparticipant':
                $gjid = $this->ReadLine($client);
                $participant = $this->ReadLine($client);
                $result = $this->SendPromoteParticipant($gjid, $participant);
                $this->WriteObject ($client, $result);
                break;
            case 'senddemoteparticipant':
                $gjid = $this->ReadLine($client);
                $participant = $this->ReadLine($client);
                $result = $this->SendDemoteParticipant($gjid, $participant);
                $this->WriteObject ($client, $result);
                break;
            case 'createmessageid':
                $result = $this->CreateMessageId ();
                $this->WriteLine ($client, $result);
                break;
            case 'sendmessage':
                $target  = $this->ReadLine($client);
                $message = $this->ReadLine($client);
                $id = $this->ReadLine($client);
                $result = $this->SendMessage ($target, $message, $id);
                $this->WriteObject ($client, $result);
                break;
            case 'sendmessageread':
                $to = $this->ReadLine($client);
                $id = $this->ReadLine($client);
                $this->SendMessageRead($to, $id);
                $this->WriteLine ($client, 'OK');
                break;
            case 'sendmessagereadbatch':
                $to = $this->ReadLine($client);
                $ids = $this->ReadArray($client);
                $this->SendMessageReadBatch($to, $ids);
                $this->WriteLine ($client, 'OK');
                break;
            case 'sendgroupmessageread':
                $to = $this->ReadLine($client);
                $id = $this->ReadLine($client);
                $participant = $this->ReadLine($client);
                $this->SendGroupMessageRead($to, $id, $participant);
                $this->WriteLine ($client, 'OK');
                break;
            case 'sendgroupmessagereadbatch':
                $to = $this->ReadLine($client);
                $ids = $this->ReadArray($client);
                $participant = $this->ReadLine($client);
                $this->SendGroupMessageReadBatch($to, $ids, $participant);
                $this->WriteLine ($client, 'OK');
                break;
            case 'sendmessagedelivered':
                $to = $this->ReadLine($client);
                $id = $this->ReadLine($client);
                $this->SendMessageDelivered($to, $id);
                $this->WriteLine ($client, 'OK');
                break;
            case 'sendmessagedeliveredbatch':
                $to = $this->ReadLine($client);
                $ids = $this->ReadArray($client);
                $this->SendMessageDeliveredBatch($to, $ids);
                $this->WriteLine ($client, 'OK');
                break;
            case 'sendgroupmessagedelivered':
                $to = $this->ReadLine($client);
                $id = $this->ReadLine($client);
                $participant = $this->ReadLine($client);
                $this->SendGroupMessageDelivered($to, $id, $participant);
                $this->WriteLine ($client, 'OK');
                break;
            case 'sendgroupmessagedeliveredbatch':
                $to = $this->ReadLine($client);
                $ids = $this->ReadArray($client);
                $participant = $this->ReadLine($client);
                $this->SendGroupMessageDeliveredBatch($to, $ids, $participant);
                $this->WriteLine ($client, 'OK');
                break;
            case 'sendmessageaudio':
                $to             = $this->ReadLine($client);
                $audioURL       = $this->ReadLine($client);
                $voice          = $this->ReadBool($client);
                $id             = $this->ReadLine($client);
                $storeURLmedia  = $this->ReadBool($client);
                $file_size      = $this->ReadInt ($client);
                $file_hash      = $this->ReadLine($client);

                $result = $this->SendMessageAudio($to, $audioURL, $voice, $id, $storeURLmedia, $file_size, $file_hash);
                $this->WriteObject ($client, $result);
                break;
            case 'sendmessagecomposing':
                $to = $this->ReadLine($client);
                $this->SendMessageComposing($to);
                $this->WriteLine ($client, 'OK');
                break;
            case 'sendmessagepaused':
                $to = $this->ReadLine($client);
                $this->SendMessagePaused($to);
                $this->WriteLine ($client, 'OK');
                break;
            case 'sendmessageimage':
                $to              = $this->ReadLine($client);
                $imageURL        = $this->ReadLine($client);
                $caption         = $this->ReadLine($client);
                $messageId       = $this->ReadLine($client);
                $storeURLmedia   = $this->ReadBool($client);
                $file_size       = $this->ReadInt($client);
                $file_hash       = $this->ReadLine($client);

                $result = $this->SendMessageImage($to, $imageURL, $caption, $messageId, $storeURLmedia, $file_size, $file_hash);
                $this->WriteObject ($client, $result);
                break;
            case 'sendmessagelocation':
                $to         = $this->ReadLine($client);
                $latitude   = $this->ReadLine($client);
                $longitude  = $this->ReadLine($client);
                $name       = $this->ReadLine($client);
                $url        = $this->ReadLine($client);
                $messageId  = $this->ReadLine($client);

                $result = $this->SendMessageLocation($to, $latitude, $longitude, $name, $url, $messageId);
                $this->WriteObject ($client, $result);
                break;
            case 'sendmessagevideo':
                $to              = $this->ReadLine($client);
                $imageURL        = $this->ReadLine($client);
                $caption         = $this->ReadLine($client);
                $messageId       = $this->ReadLine($client);
                $storeURLmedia   = $this->ReadBool($client);
                $file_size       = $this->ReadInt($client);
                $file_hash       = $this->ReadLine($client);
                
                $result = $this->SendMessageVideo($to, $imageURL, $caption, $messageId, $storeURLmedia, $file_size, $file_hash);
                $this->WriteObject ($client, $result);
                break;
            case 'sendupdatenickname':
                $nickname = $this->ReadLine($client);
                $this->UpdateNickname($nickname);
                $this->WriteLine ($client, 'OK');
                break;
            case 'sendgetpresences':
                $to = $this->ReadArray($client);
                $result = $this->SendGetPresences($to);
                $this->WriteObject($client, $result);
                break;
            case 'sendsetprivacyblockedlist':
                $blockedJids = $this->ReadArray($client);
                $this->SendSetPrivacyBlockedList($blockedJids);
                $this->WriteLine ($client, 'OK');
                break;
            case 'sendgetprivacyblockedlist':
                $result = $this->SendGetPrivacyBlockedList();
                $this->WriteObject ($client, $result);
                break;
            case 'sendsetprofilepicture':
                $path = $this->ReadLine($client);
                $result = $this->SendSetProfilePicture($path);
                $this->WriteObject($client, $result);
                break;
            case 'sendremoveprofilepicture':
                $result = $this->SendRemoveProfilePicture();
                $this->WriteObject($client, $result);
                break;
            case 'sendstatusupdate':
                $text = $this->ReadLine($client);
                $result = $this->SendStatusUpdate($text);
                $this->WriteObject($client, $result);
                break;
            case 'sendvcard':
                $to = $this->ReadLine($client);
                $vCard = $this->ReadLine($client);
                $name = $this->ReadLine($client);
                $id = $this->ReadLine($client);
                $result = $this->SendVcard($to, $vCard,$name, $id);
                $this->WriteObject($client, $result);
                break;
            case 'sendsync':
                $numbers = $this->ReadArray($client);
                $deletedNumbers = $this->ReadArray($client);
                $syncType = $this->ReadInt($client);
                $result = $this->SendSync($numbers, $deletedNumbers, $syncType);
                $this->WriteObject($client, $result);
                break;
            case 'checkcredentials':
                $res = $this->CheckCredentials();
                $this->WriteObject ($client, $res);
                break;
            case 'coderegister':
                $code = $this->ReadLine($client);
                $res = $this->CodeRegister($code);
                $this->WriteObject ($client, $res);
                break;
            case 'coderequest':
                $method = $this->ReadLine($client);
                $res = $this->CodeRequest($method);
                $this->WriteObject ($client, $res);
                break;
            case 'quit':
                return true;
        }
        return false;
    }

    function CreateRequestId ()
    {
        return $this->wa->createRequestId ();
    }

    function PeekEvents ($client, $forcePeek = false)
    {
        // Ensure PollMessages was called.
        if (!$this->everPolledMessages || $forcePeek) {
            $this->SafePollMessage($forcePeek);
        }
        // Flush any server events
        $event = $this->PopEvent ();
        while (!empty($event))
        {
            $name = $event ['name'];
            $data = $event ['data'];
            $this->WriteLine ($client, $name);
            $this->WriteObject ($client, $data);
            $event = $this->PopEvent ();
        }

        $this->forcedEventFlushed = true;
    }

    function GetEventIndex ($id)
    {
        if ($this->eventQueue->isEmpty() || $id == null)
            return -1;

        $result = null;
        $this->eventQueue->rewind();
        
        while ($this->eventQueue->valid()) {
            $event = $this->eventQueue->current();
            $data  = $event ['data'];

            if (!isset($data ['id'])) {
                $this->eventQueue->next();
                continue;
            }

            if ($data ['id'] == $id) {
                $index = $this->eventQueue->key();
                return $index;
            }
            $this->eventQueue->next();
        }
        $this->eventQueue->rewind();
        return -1;
    }

    function GetEventFromIndex ($index)
    {
        if ($index == -1 || !$this->eventQueue->offsetExists ($index))
            return null;
        return $this->eventQueue->offsetGet ($index);
    }

    function ReplaceEventAtIndex ($index, $event)
    {
        $this->eventQueue->offsetSet ($index, $event);
    }

    function GetEventResult ($id)
    {
        if ($this->eventQueue->isEmpty()) {
            return null;
        }

        $result = null;
        $streamError = null;

        $event = $this->eventQueue->top();
        $data  = $event ['data'];

        if ($data ['id'] == $id) {

            if (empty($data ['code']))
                $data['code'] = '200';

            $result = $data;
            $index = $this->eventQueue->key();
            $this->eventQueue->offsetUnset($index);

        } else {

            $this->eventQueue->rewind();

            while ($this->eventQueue->valid()) {
                $event = $this->eventQueue->current();
                $data = $event ['data'];

                if (!isset($data ['id'])) {
                    $this->eventQueue->next();
                    continue;
                }


                if ($data ['id'] == $id) {
                    if (empty($data ['code']))
                        $data['code'] = '200';

                    $result = $data;
                    $index = $this->eventQueue->key();
                    $this->eventQueue->offsetUnset($index);
                    break;
                }
                //
                // If some stream error happened, we will return the result as 500 - Stream error
                // we do not break the loop because maybe we got a result before the Stream error
                if ($event ['name'] == 'onstreamerror')
                    $streamError = $data;
                $this->eventQueue->next();
            }
        }

        $this->eventQueue->rewind();

        if ($result == null && $streamError != null)
            $result = $streamError;
        return $result;
    }

    function SendActiveStatus ()
    {
        $this->isActive = true;
        $this->wa->sendActiveStatus();
    }

    function GetConnectedStatus ()
    {
        if (!$this->IsConnected())
            return 'unknown';
        if (!$this->isActive)
            return 'offline';
        return 'online';
    }

    function SendOfflineStatus()
    {
        $this->wa->sendOfflineStatus();
        $this->isActive = false;
    }

    function SendGetGroups ()
    {
        $id = $this->CreateRequestId ();

        $this->wa->sendGetGroups($id);

        return $this->GetEventResult ($id);
    }

    function SendChangeNumber($number)
    {
        $id = $this->CreateRequestId ();

        $registration = $this->GetRegistration();

        $this->wa->sendChangeNumber($number, $registration->getIdentity(), $id);

        return $this->GetEventResult ($id);
    }

    function SendGetClientConfig()
    {
        $id = $this->CreateRequestId ();

        $this->wa->sendGetClientConfig($id);
        
        return $this->GetEventResult ($id);
    }

    function SendGetGroupV2Info ($groupId)
    {
        $id = $this->CreateRequestId ();

        $this->wa->sendGetGroups($groupId, $id);

        return $this->GetEventResult ($id);
    }

    function SendGetPrivacyBlockedList ()
    {
        $id = $this->CreateRequestId ();

        $this->wa->sendGetPrivacyBlockedList($id);

        return $this->GetEventResult ($id);
    }

    function SendGetPrivacySettings ()
    {
        $id = $this->CreateRequestId ();

        $this->wa->sendGetPrivacySettings($id);

        return $this->GetEventResult ($id);
    }

    function SendSetPrivacySettings ($category, $value)
    {
        $id = $this->CreateRequestId ();

        $this->wa->sendSetPrivacySettings($category, $value, $id);

        return $this->GetEventResult ($id);
    }

    private function TryGetCachedProfilePicture($type, $number)
    {
        $filename = $this->GetProfilePicturePath ($type, $number);
        if (!file_exists($filename))
            return null;
        $creation_time = @filectime($filename);
        if ($creation_time === FALSE)
            return null;
        $now = time();
        // Avoid issues with server with wrong clock.
        if ($creation_time > $now)
            return null;
        $delta_seconds = $now - $creation_time;
        $timeout = 15 * 60;
        if ($delta_seconds > $timeout)
            return null;
        return ['code'=>'200', 'filename'=> $filename];
    }

    function SendGetProfilePicture ($number, $type)
    {
        $id = $this->CreateRequestId ();

        $cached_result = $this->TryGetCachedProfilePicture ($type, $number);

        if ($cached_result != null)
            return $cached_result;

        if ($type == 'preview')
            $this->wa->sendGetProfilePicture($number, false, $id);
        else
            $this->wa->sendGetProfilePicture($number, true, $id);

        return $this->GetEventResult ($id);
    }

    function SendGetServerProperties ()
    {
        $id = $this->CreateRequestId ();

        $this->wa->sendGetServerProperties($id);

        return $this->GetEventResult ($id);
    }

    function SendExtendAccount ()
    {
        $id = $this->CreateRequestId ();

        $this->wa->sendExtendAccount($id);

        return $this->GetEventResult ($id);
    }

    function SendGetBroadcastLists ()
    {
        $id = $this->CreateRequestId ();

        $this->wa->sendGetBroadcastLists($id);

        return $this->GetEventResult ($id);
    }

    function SendRemoveAccount ($lg, $lc, $feedback)
    {
        $id = $this->CreateRequestId ();

        $this->wa->sendRemoveAccount($lg, $lc, $feedback, $id);

        return $this->GetEventResult ($id);
    }

    function SendGetStatuses ($jids)
    {
        $id = $this->CreateRequestId ();

        $this->wa->sendGetStatuses($jids, $id);

        return $this->GetEventResult ($id);
    }

    function SendGroupsChatCreate ($subject, $participants)
    {
        $id = $this->CreateRequestId ();

        $this->wa->sendGroupsChatCreate($subject, $participants, $id);

        return $this->GetEventResult ($id);
    }

    function SendSetGroupSubject ($gjid, $subject)
    {
        $id = $this->CreateRequestId ();

        $this->wa->sendSetGroupSubject ($gjid, $subject, $id);

        return $this->GetEventResult ($id);
    }

    function SendGroupsLeave  ($gjid)
    {
        $id = $this->CreateRequestId ();

        $this->wa->sendGroupsLeave ($gjid,  $id);

        return $this->GetEventResult ($id);
    }

    function  SendGroupsParticipantAdd ($groupId, $participant)
    {
        $id = $this->CreateRequestId ();

        $this->wa->sendGroupsParticipantsAdd($groupId, $participant, $id);

        return $this->GetEventResult ($id);
    }

    function SendGroupsParticipantRemove ($groupId, $participant)
    {
        $id = $this->CreateRequestId ();

        $this->wa->sendGroupsParticipantsRemove($groupId, $participant, $id);

        return $this->GetEventResult ($id);
    }

    function SendPromoteParticipant ($gId, $participant)
    {
        $id = $this->CreateRequestId ();

        $this->wa->sendPromoteParticipants ($gId, $participant, $id);

        return $this->GetEventResult ($id);
    }

    function SendDemoteParticipant ($gId, $participant)
    {
        $id = $this->CreateRequestId ();

        $this->wa->sendDemoteParticipants($gId, $participant, $id);

        return $this->GetEventResult ($id);
    }

    function CreateMessageId ()
    {
        return $this->wa->createMessageId ();
    }

    function SendMessage ($target, $message, $id = null)
    {
        if (empty($id))
            $id = $this->CreateMessageId ();

        $this->wa->sendMessage($target , $message, false,  $id);

        return $this->GetEventResult ($id); 
    }

    function SendMessageRead ($to, $id)
    {
        $this->wa->sendMessageRead($to, $id);
    }

    function SendMessageReadBatch ($to, $ids)
    {
        $this->wa->sendMessageRead($to, $ids);
    }

    function SendGroupMessageRead ($to, $id, $participant)
    {
        $this->wa->sendMessageRead($to, $id, 'read', $participant);
    }

    function SendGroupMessageReadBatch ($to, $ids, $participant)
    {
        $this->wa->sendMessageRead($to, $ids, 'read', $participant);
    }

    function SendGroupMessageDelivered ($to, $id, $participant)
    {
        $this->wa->sendMessageRead($to, $id, null, $participant);
    }

    function SendGroupMessageDeliveredBatch ($to, $ids, $participant)
    {
        $this->wa->sendMessageRead($to, $ids, null, $participant);
    }

    function SendMessageDelivered ($to, $id)
    {
        $this->wa->sendMessageRead($to, $id, null);
    }

    function SendMessageDeliveredBatch ($to, $ids)
    {
        $this->wa->sendMessageRead($to, $ids, null);
    }

    function SendMessageComposing($to)
    {
        $this->wa->sendMessageComposing($to);
    }

    function SendMessagePaused($to)
    {
        $this->wa->sendMessagePaused($to);
    }

    function SendMessageAudio($to, $audioURL, $voice = false, $id = null, $storeURLmedia = false, $file_size = 0, $file_hash = '')
    {
         if (empty($id))
            $id = $this->CreateMessageId ();

        if (empty($audioURL) || !CheckFile::Exists($audioURL))
            return ['message' => 'Could not find '. $audioURL,'code' => '400'];

        $messageId = $this->wa->sendMessageAudio($to, $audioURL, $storeURLmedia, $file_size, $file_hash, $voice, $id);

        $event_result = $this->GetEventResult ($id);
        if ($event_result != null)
            return $event_result;
        if ($messageId != null)
            return ['message' => 'Error sending audio','code' => '500'];
        return ['message' => 'Error sending audio','code' => '400'];
    }

    function SendMessageImage($to, $imageURL, $caption = '', $id = null, $storeURLmedia = false, $file_size = 0, $file_hash = '')
    {
        if (empty($id))
            $id = $this->CreateMessageId ();

        if (empty($imageURL) || !CheckFile::Exists($imageURL))
            return ['message' => 'Could not find ('. $imageURL.')' ,'code' => '400'];

        $messageId = $this->wa->sendMessageImage($to, $imageURL, $storeURLmedia, $file_size, $file_hash, $caption, $id);

        $event_result = $this->GetEventResult ($id);
        if ($event_result != null)
            return $event_result;
        if ($messageId != null)
            return ['message' => 'Error sending image','code' => '500'];
        return ['message' => 'Error sending image','code' => '400'];
    }

    function SendMessageLocation($to, $latitude, $longitude, $name = '', $url = '', $id = null)
    {
        if (empty($id))
            $id = $this->CreateMessageId ();

        $this->wa->sendMessageLocation($to, $longitude, $latitude, $name, $url, $id);

        return $this->GetEventResult ($id); 
    }

    function SendMessageVideo($to, $imageURL, $caption = '', $id = null, $storeURLmedia = false, $file_size = 0, $file_hash = '')
    {
        if (empty($id))
            $id = $this->CreateMessageId ();

        if (empty($imageURL) || !CheckFile::Exists($imageURL))
            return ['message' => 'Could not find ('. $imageURL.')', 'code' => '400'];

        $messageId = $this->wa->sendMessageVideo($to, $imageURL, $storeURLmedia, $file_size, $file_hash, $caption, $id);

        $event_result = $this->GetEventResult ($id);
        if ($event_result != null)
            return $event_result;
        if ($messageId != null)
            return ['message' => 'Error sending video','code' => '500'];
        return ['message' => 'Error sending video','code' => '400'];
    }
    // This method update the Nickname
    // There is no way to update the nickname if we are not in the 'Online' status
    // in this case we need to cleanup the connection and reconnect again using a new nickname
    function UpdateNickname($nickname)
    {
        if ($this->isActive) {
            $this->wa->sendAvailableForChat($nickname);
            return;
        }
        $this->Cleanup();
        $this->Connect($this->number, $nickname, $this->autoReplyMode);
    }

    function SendGetPresences($to)
    {
        if (!$this->isActive)
            return ['message' => 'You need to be online to subscribe presences ','code' => '400'];

        if (!is_array($to))
            $numbers = [$to];
        else
            $numbers = $to;

        foreach ($numbers as $number)
            $this->wa->sendPresenceSubscription($number);

        $this->SafePollMessage ();

        foreach ($numbers as $number)
            $this->wa->sendPresenceUnsubscription($number);

        $results = $this->GetEventResult ('onpresence');

        return $results;
    }

    function SendSetGroupPicture($gjid, $path)
    {
        $id = $this->CreateRequestId ();

        $this->wa->sendSetGroupPicture($gjid, $path, $id);

        return $this->GetEventResult ($id);
    }

    function SendSetPrivacyBlockedList($blockedJids)
    {
        $this->wa->sendSetPrivacyBlockedList($blockedJids);
    }

    function SendSetProfilePicture($path)
    {
        if (empty($path) || !file_exists($path))
            return ['message' => 'Could not find '. $path,'code' => '400'];

        $id = $this->CreateRequestId ();

        $this->wa->sendSetProfilePicture($path, $id);

        return $this->GetEventResult ($id);
    }

    function SendRemoveProfilePicture()
    {
        $id = $this->CreateRequestId ();

        $this->wa->sendRemoveProfilePicture($id);

        return $this->GetEventResult ($id);
    }

    function SendStatusUpdate($txt)
    {
        $id = $this->CreateRequestId ();

        $this->wa->sendStatusUpdate($txt, $id);

        return $this->GetEventResult ($id);
    }

    function SendVcard($to, $vCard, $name, $id = null)
    {
        if (empty($id))
            $id = $this->CreateMessageId ();

        $this->wa->sendVcard($to, $name, $vCard, $id);

        return $this->GetEventResult ($id);
    }

    function SendSync(array $numbers, array $deletedNumbers = null, $syncType = 3)
    {
        $id = $this->CreateRequestId ();

        $this->wa->sendSync($numbers, $deletedNumbers, $syncType , $id);

        return $this->GetEventResult ($id);
    }

    function CheckCredentials()
    {
        $registration = $this->GetRegistration();
        if ($registration == null)
            return ['message' => 'Error checking credentials, no number set','code' => '500'];

        $id = 'check_credentials';

        try {
            $registration->checkCredentials($id);
        }
        catch (Exception $e)
        {
            $error = $e->getMessage();
        }

        $result = $this->GetEventResult ($id);

        if (!empty($error)) {
            if (empty($result ['code']))
                $result ['code'] = '400';
            $result ['error'] = $error;
        }

        return $result;
    }

    function CodeRegister($code)
    {
        $registration = $this->GetRegistration();
        if ($registration == null)
            return ['message' => 'Error registering code, no number set','code' => '500'];

        $code = str_replace('-', '', $code);
        $code = trim($code);

        $id = 'code_register';
        $error = null;

        try {
            $registration->codeRegister($code, $id);
        } 
        catch (Exception $e)
        {
            $error = $e->getMessage();
        }

        $result = $this->GetEventResult ($id);

        if (!empty($error)) {
            if (empty($result ['code']))
                $result ['code'] = '400';
            $result ['error'] = $error;
        }

        return $result;
    }

    function CodeRequest($method)
    {
        $registration = $this->GetRegistration();
        if ($registration == null)
            return ['message' => 'Error requsting code, no number set','code' => '500'];

        $id = 'code_request';
        $error = null;

        try {
            $registration->codeRequest($id, $method);
        } 
        catch (Exception $e)
        {
            $error = $e->getMessage();
        }

        $result = $this->GetEventResult ($id);

        if (!empty($error)) {
            if (empty($result ['code']))
                $result ['code'] = '400';
            $result ['error'] = $error;
        }
        return $result;
    }
}

?>
