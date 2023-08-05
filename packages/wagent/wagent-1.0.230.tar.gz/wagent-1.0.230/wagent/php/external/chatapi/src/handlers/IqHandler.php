<?php

require_once 'Handler.php';
if (extension_loaded('curve25519') && extension_loaded('protobuf')) {
    require_once __DIR__.'/../libaxolotl-php/protocol/SenderKeyDistributionMessage.php';
    require_once __DIR__.'/../libaxolotl-php/groups/GroupSessionBuilder.php';
    require_once __DIR__.'/../pb_wa_messages.php';
}
require_once __DIR__.'/../protocol.class.php';
require_once __DIR__.'/../Constants.php';
require_once __DIR__.'/../func.php';

class IqHandler implements Handler
{
    protected $node;
    protected $parent;
    protected $phoneNumber;

    public function __construct($parent, $node)
    {
        $this->node = $node;
        $this->parent = $parent;
        $this->phoneNumber = $this->parent->getMyNumber();
    }

    public function Process()
    {
        if ($this->node->getChild('query') != null) {
            if (isset($this->parent->getNodeId()['privacy']) && ($this->parent->getNodeId()['privacy'] == $this->node->getAttribute('id'))) {
                $listChild = $this->node->getChild(0)->getChild(0);
                foreach ($listChild->getChildren() as $child) {
                    $blockedJids[] = $child->getAttribute('value');
                }
                $this->parent->eventManager()->fire('onGetPrivacyBlockedList',
                [
                    $this->phoneNumber,
                    $this->node->getAttribute('id'),
                    $blockedJids,
                ]);
                unset($this->parent->getNodeId()['privacy']);
                return;
            }
        }

        if (isset($this->parent->getNodeId()['participantadd']) && $this->parent->getNodeId()['participantadd'] == $this->node->getAttribute('id')) {
            $jid = $this->node->getChild(0)->getChild(0)->getAttribute('jid');
            $this->parent->eventManager()->fire('onParticipantAdded',
            [
                $this->phoneNumber,
                $this->node->getAttribute('from'),
                $jid,
                $this->node->getAttribute('id'),
            ]);
            unset($this->parent->getNodeId()['participantadd']);
            return;
        }

        if (isset($this->parent->getNodeId()['participantremove']) && $this->parent->getNodeId()['participantremove'] == $this->node->getAttribute('id')) {
            $jid = $this->node->getChild(0)->getChild(0)->getAttribute('jid');
            $this->parent->eventManager()->fire('onParticipantRemove',
            [
                $this->phoneNumber,
                $this->node->getAttribute('from'),
                $jid,
                $this->node->getAttribute('id'),
            ]);
            unset($this->parent->getNodeId()['participantremove']);
            return;
        }

        if (isset($this->parent->getNodeId()['setpicture']) && $this->parent->getNodeId()['setpicture'] == $this->node->getAttribute('id')) {
            $this->parent->eventManager()->fire('onSetPicture',
            [
                $this->phoneNumber,
                $this->node->getAttribute('id'),
            ]);
            unset($this->parent->getNodeId()['setpicture']);
            return;
        }

        if (isset($this->parent->getNodeId()['statusupdate']) && $this->parent->getNodeId()['statusupdate'] == $this->node->getAttribute('id')) {
            $this->parent->eventManager()->fire('onStatusUpdate',
            [
                $this->phoneNumber,
                $this->node->getAttribute('id'),
            ]);
            unset($this->parent->getNodeId()['statusupdate']);
            return;
        }

        $promoteElement = $this->node->getChild('promote');
        if ($promoteElement != null) {
            $promotedJIDs = [];
            foreach ($promoteElement->getChildren() AS $cn)
                $promotedJIDs[] = $cn->getAttribute('jid');
            $this->parent->eventManager()->fire('onParticipantsPromote',
            [
                $this->phoneNumber,
                $this->node->getAttribute('id'),
                $this->node->getAttribute('from'),
                $promotedJIDs,
            ]);
        }

        $demoteElement = $this->node->getChild('demote');
        if ($demoteElement != null) {
            $demotedJIDs = [];
            foreach ($demoteElement->getChildren() AS $cn)
                $demotedJIDs[] = $cn->getAttribute('jid');
            $this->parent->eventManager()->fire('onParticipantsDemote',
            [
                $this->phoneNumber,
                $this->node->getAttribute('id'),
                $this->node->getAttribute('from'),
                $demotedJIDs,
            ]);
        }

        $configElement = $this->node->getChild('config');
        if ($configElement != null) {
            $this->parent->eventManager()->fire('onGetClientConfig',
                [
                    $this->phoneNumber,
                    $this->node->getAttribute('id'),
                    $configElement->getAttribute('platform'),
                    $configElement->getAttribute('id'),
                    $configElement->getAttribute('lg'),
                    $configElement->getAttribute('lc'),
                    $configElement->getAttribute('preview'),
                    $configElement->getAttribute('default'),
                    $configElement->getAttribute('groups'),
                    $configElement->getAttribute('call'),
                ]);
        }

        $privacyElement = $this->node->getChild('privacy');
        if ($privacyElement != null) {
            $values = [];

            foreach ($privacyElement->getChildren() as $child) {
                $name  = $child->getAttribute('name');
                $value = $child->getAttribute('value');
                $values [$name] = $value;
            }

            $this->parent->eventManager()->fire('onGetPrivacySettings',
                [
                    $this->phoneNumber,
                    $this->node->getAttribute('id'),
                    $values,
                ]);
        }

        if ($this->node->getAttribute('type') == 'get'
    && $this->node->getAttribute('xmlns') == 'urn:xmpp:ping') {
            $this->parent->eventManager()->fire('onPing',
        [
            $this->phoneNumber,
            $this->node->getAttribute('id'),
        ]);
            $this->parent->sendPong($this->node->getAttribute('id'));
        }

        if ($this->node->getChild('sync') != null) {

    //sync result
    $sync = $this->node->getChild('sync');
            $existing = $sync->getChild('in');
            $nonexisting = $sync->getChild('out');

    //process existing first
    $existingUsers = [];
            if (!empty($existing)) {
                foreach ($existing->getChildren() as $child) {
                    $existingUsers[$child->getData()] = $child->getAttribute('jid');
                }
            }

    //now process failed numbers
    $failedNumbers = [];
            if (!empty($nonexisting)) {
                foreach ($nonexisting->getChildren() as $child) {
                    $failedNumbers[] = str_replace('+', '', $child->getData());
                }
            }

            $index = $sync->getAttribute('index');

            $result = new SyncResult($index, $sync->getAttribute('sid'), $existingUsers, $failedNumbers);

            $this->parent->eventManager()->fire('onGetSyncResult',
        [
            $result,
            $this->node->getAttribute('id')
        ]);
        }

        if ($this->node->getChild('props') != null) {
            //server properties
        $props = [];
            foreach ($this->node->getChild(0)->getChildren() as $child) {
                $props[$child->getAttribute('name')] = $child->getAttribute('value');
            }
            $this->parent->eventManager()->fire('onGetServerProperties',
            [
                $this->phoneNumber,
                $this->node->getAttribute('id'),
                $this->node->getChild(0)->getAttribute('version'),
                $props,
            ]);
        }
        if ($this->node->getChild('picture') != null) {
            $this->parent->eventManager()->fire('onGetProfilePicture',
            [
                $this->phoneNumber,
                $this->node->getAttribute('id'),
                $this->node->getAttribute('from'),
                $this->node->getChild('picture')->getAttribute('type'),
                $this->node->getChild('picture')->getData(),
            ]);
        }
        if ($this->node->getChild('media') != null || $this->node->getChild('duplicate') != null) {
            $this->parent->processUploadResponse($this->node);
        }
        if (strpos($this->node->getAttribute('from'), Constants::WHATSAPP_GROUP_SERVER) !== false) {
            //There are multiple types of Group reponses. Also a valid group response can have NO children.
        //Events fired depend on text in the ID field.
        $groupList = [];
            $groupNodes = [];
            if ($this->node->getChild(0) != null && $this->node->getChild(0)->getChildren() != null) {
                foreach ($this->node->getChild(0)->getChildren() as $child) {
                    $groupList[] = $child->getAttributes();
                    $groupNodes[] = $child;
                }
            }
            if (isset($this->parent->getNodeId()['groupcreate']) && ($this->parent->getNodeId()['groupcreate'] == $this->node->getAttribute('id'))) {
                $this->parent->setGroupId($this->node->getChild(0)->getAttribute('id'));
                $this->parent->eventManager()->fire('onGroupsChatCreate',
                [
                    $this->phoneNumber,
                    $this->node->getChild(0)->getAttribute('id'),
                    $this->node->getAttribute('id')
                ]);
                unset($this->parent->getNodeId()['groupcreate']);
            }
            if (isset($this->parent->getNodeId()['leavegroup']) && ($this->parent->getNodeId()['leavegroup'] == $this->node->getAttribute('id'))) {
                $this->parent->setGroupId($this->node->getChild(0)->getChild(0)->getAttribute('id'));
                $this->parent->eventManager()->fire('onGroupsChatEnd',
                [
                    $this->phoneNumber,
                    $this->node->getChild(0)->getChild(0)->getAttribute('id'),
                    $this->node->getAttribute('id')
                ]);
                unset($this->parent->getNodeId()['leavegroup']);
            }
            if (isset($this->parent->getNodeId()['getgroups']) && ($this->parent->getNodeId()['getgroups'] == $this->node->getAttribute('id'))) {
                $this->parent->eventManager()->fire('onGetGroups',
                [
                    $this->phoneNumber,
                    $this->node->getAttribute('id'),
                    $groupList,
                ]);
                //getGroups returns a array of nodes which are exactly the same as from getGroupV2Info
                //so lets call this event, we have all data at hand, no need to call getGroupV2Info for every
                //group we are interested
                foreach ($groupNodes as $groupNode) {
                    $this->handleGroupV2InfoResponse($groupNode, true, $this->node->getAttribute('id'));
                }
                unset($this->parent->getNodeId()['getgroups']);
            }
            if (isset($this->parent->getNodeId()['get_groupv2_info']) && ($this->parent->getNodeId()['get_groupv2_info'] == $this->node->getAttribute('id'))) {
                $groupChild = $this->node->getChild(0);
                if ($groupChild != null) {
                    $this->handleGroupV2InfoResponse($groupChild);
                }
                unset($this->parent->getNodeId()['get_groupv2_info']);
            }
        }
        if (isset($this->parent->getNodeId()['get_lists']) && ($this->parent->getNodeId()['get_lists'] == $this->node->getAttribute('id'))) {
            $broadcastLists = [];
            if ($this->node->getChild(0) != null) {
                $childArray = $this->node->getChildren();
                foreach ($childArray as $list) {
                    if ($list->getChildren() != null) {
                        foreach ($list->getChildren() as $sublist) {
                            $id = $sublist->getAttribute('id');
                            $name = $sublist->getAttribute('name');
                            $broadcastLists[$id]['name'] = $name;
                            $recipients = [];
                            foreach ($sublist->getChildren() as $recipient) {
                                array_push($recipients, $recipient->getAttribute('jid'));
                            }
                            $broadcastLists[$id]['recipients'] = $recipients;
                        }
                    }
                }
            }
            $this->parent->eventManager()->fire('onGetBroadcastLists',
            [
                $this->phoneNumber,
                $broadcastLists,
            ]);
            unset ($this->parent->getNodeId()['get_lists']);
        }
        if ($this->node->getChild('pricing') != null) {
            $this->parent->eventManager()->fire('onGetServicePricing',
            [
                $this->phoneNumber,
                $this->node->getChild(0)->getAttribute('price'),
                $this->node->getChild(0)->getAttribute('cost'),
                $this->node->getChild(0)->getAttribute('currency'),
                $this->node->getChild(0)->getAttribute('expiration'),
            ]);
        }
        if ($this->node->getChild('extend') != null) {
            $this->parent->eventManager()->fire('onGetExtendAccount',
            [
                $this->phoneNumber,
                $this->node->getChild('account')->getAttribute('kind'),
                $this->node->getChild('account')->getAttribute('status'),
                $this->node->getChild('account')->getAttribute('creation'),
                $this->node->getChild('account')->getAttribute('expiration'),
            ]);
        }
        if ($this->node->getChild('normalize') != null) {
            $this->parent->eventManager()->fire('onGetNormalizedJid',
            [
                $this->phoneNumber,
               $this->node->getChild(0)->getAttribute('result'),
            ]);
        }
        if ($this->node->getChild('status') != null) {
            $status = $this->node->getChild('status');
            $arrStatus = [];
            $children = $status->getChildren();
            if (!empty($children)) {
                foreach($children as $user)
                {
                    $item = [];
                    $item ['from']  =  $user->getAttribute('jid');
                    $t = $user->getAttribute('t');
                    if (!empty($t))
                        $item ['t'] = $t;
                    $type = $user->getAttribute('type');
                    if (!empty($type))
                        $item ['type'] = $type;
                    $code = $user->getAttribute('code');
                    if (!empty($code))
                        $item ['code'] = $code;
                    $data = $user->getData();
                    if (!empty($data))
                        $item ['data'] = $data;
                    $arrStatus [] = $item;
                }
            }

            $this->parent->eventManager()->fire('onGetStatuses',
            [
                    $this->phoneNumber,
                    $this->node->getAttribute('id'),
                    $arrStatus
            ]);
        }
        if (($this->node->getAttribute('type') == 'error') && ($this->node->getChild('error') != null)) {
            $errorType = null;
            $this->parent->logFile('error', 'Iq error with {id} id', ['id' => $this->node->getAttribute('id')]);
            foreach ($this->parent->getNodeId() as $type => $nodeID) {
                if ($nodeID == $this->node->getAttribute('id')) {
                    $errorType = $type;
                    break;
                }
            }
            $nodeIds = $this->parent->getNodeId();
            if (isset($nodeIds['sendcipherKeys']) && (isset($nodeIds['sendcipherKeys'])  ==  $this->node->getAttribute('id'))  && $this->node->getChild('error')->getAttribute('code') == '406') {
                $this->parent->sendSetPreKeys();
            } elseif ($this->node->getAttribute('id') == '2'){
                $this->parent->sendSetGCM();
            }

            $this->parent->eventManager()->fire('onGetError',
            [
                $this->phoneNumber,
                $this->node->getAttribute('from'),
                $this->node->getAttribute('id'),
                $this->node->getChild(0),
                $errorType,
            ]);
        }

        if (isset($this->parent->getNodeId()['cipherKeys']) && ($this->parent->getNodeId()['cipherKeys'] == $this->node->getAttribute('id'))) {
            $users = $this->node->getChild(0)->getChildren();
            foreach ($users as $user) {
                $jid = $user->getAttribute('jid');
                $registrationId = deAdjustId($user->getChild('registration')->getData());
                $identityKey = new  IdentityKey(new DjbECPublicKey($user->getChild('identity')->getData()));
                $signedPreKeyId = deAdjustId($user->getChild('skey')->getChild('id')->getData());
                $signedPreKeyPub = new DjbECPublicKey($user->getChild('skey')->getChild('value')->getData());
                $signedPreKeySig = $user->getChild('skey')->getChild('signature')->getData();
                $preKeyId = deAdjustId($user->getChild('key')->getChild('id')->getData());
                $preKeyPublic = new DjbECPublicKey($user->getChild('key')->getChild('value')->getData());

                $preKeyBundle = new PreKeyBundle($registrationId, 1, $preKeyId, $preKeyPublic, $signedPreKeyId, $signedPreKeyPub, $signedPreKeySig, $identityKey);
                $sessionBuilder = new SessionBuilder($this->parent->getAxolotlStore(), $this->parent->getAxolotlStore(), $this->parent->getAxolotlStore(), $this->parent->getAxolotlStore(), ExtractNumber($jid), 1);

                $sessionBuilder->processPreKeyBundle($preKeyBundle);
                if (isset($this->parent->getPendingNodes()[ExtractNumber($jid)])) {
                    foreach ($this->parent->getPendingNodes()[ExtractNumber($jid)] as $pendingNode) {
                        $msgHandler = new MessageHandler($this->parent, $pendingNode);
                        $msgHandler->Process();
                    }
                    $this->parent->unsetPendingNode($jid);
                }
                $this->parent->sendPendingMessages($jid);
            }
        }
    }

  /**
   * @param ProtocolNode $groupNode
   * @param mixed        $fromGetGroups
   */
  protected function handleGroupV2InfoResponse(ProtocolNode $groupNode, $fromGetGroups = false, $msgId = null)
  {
      $creator = $groupNode->getAttribute('creator');
      $creation = $groupNode->getAttribute('creation');
      $subject = $groupNode->getAttribute('subject');
      $groupID = $groupNode->getAttribute('id');
      $participants = [];
      $admins = [];
      if ($groupNode->getChild(0) != null) {
          foreach ($groupNode->getChildren() as $child) {
              $participants[] = $child->getAttribute('jid');
              if ($child->getAttribute('type') == 'admin') {
                  $admins[] = $child->getAttribute('jid');
              }
          }
      }
      $this->parent->eventManager()->fire('onGetGroupV2Info',
          [
              $this->phoneNumber,
              $groupID,
              $creator,
              $creation,
              $subject,
              $participants,
              $admins,
              $fromGetGroups,
              $msgId
          ]
      );
  }
}

class SyncResult
{
    public $index;
    public $syncId;
    /** @var array $existing */
    public $existing;
    /** @var array $nonExisting */
    public $nonExisting;

    public function __construct($index, $syncId, $existing, $nonExisting)
    {
        $this->index = $index;
        $this->syncId = $syncId;
        $this->existing = $existing;
        $this->nonExisting = $nonExisting;
    }
}
