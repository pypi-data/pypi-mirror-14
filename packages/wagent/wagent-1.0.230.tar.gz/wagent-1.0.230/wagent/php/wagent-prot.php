<?php

require_once ('external/chatapi/src/whatsprot.class.php');
require_once ('external/chatapi/src/Registration.php');

class WagentProt extends WhatsProt 
{
    public function __construct($number, $nickname, $debug = false)
    {
        parent::__construct($number, $nickname, $debug);
    }

    public function createRequestId ()
    {
        return $this->createIqId();
    }

    public function createMessageId ()
    {
        return $this->createMsgId();
    }

    public function getServerReceivedId ()
    {
        return $this->serverReceivedId;
    }

    public function getPhoneNumber ()
    {
        return $this->phoneNumber;
    }


    public function getSocket ()
    {
        return $this->socket;
    }

    public static function ParseID($jid)
    {
        $parts = explode('@', $jid);
        $parts = reset($parts);
        return $parts;
    }
}

class WagentRegistration extends Registration
{
    public function __construct($number, $debug = false, $customPath = false)
    {
        parent::__construct($number, $debug, $customPath);
    }

    public function getIdentity ()
    {
        return $this->identity;
    }

}

?>