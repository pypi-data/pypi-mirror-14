import json

import pyorient
from plenum.common.util import getlogger
from sovrin.common.txn import TXN_ID
from sovrin.persistence.document_store import DocumentStore

from sovrin.persistence.orientdb_store import OrientDbStore

logger = getlogger()

TXN_DATA = "TxnData"


class NodeDocumentStore(DocumentStore):
    def classesNeeded(self):
        return [
            (TXN_DATA, self.createTxnDataClass),
        ]

    def bootstrap(self):
        self.createClasses()

    def createTxnDataClass(self):
        self.client.command("create class {}".format(TXN_DATA))
        self.createClassProperties(TXN_DATA, {
            "clientId": "string",
            "reqId": "long",
            TXN_ID: "string",
            "reply": "string",
            "serialNo": "long",
            "STH": "string",
            "auditInfo": "embeddedlist string"
        })

        # Index in case we need to access all transactions of a client
        # self.createIndexOnClass(TXN_REQ, "clientId")

        self.client.command("create index CliReq on {} (clientId, reqId) unique".
                            format(TXN_DATA))
        self.createUniqueIndexOnClass(TXN_DATA, TXN_ID)
        self.createUniqueIndexOnClass(TXN_DATA, "serialNo")

    def addReplyForTxn(self, txnId, reply, clientId, reqId):
        self.client.command("update {} set {} = '{}', reply = '{}', "
                            "clientId = '{}', reqId = {} upsert where {} = '{}'".
                            format(TXN_DATA, TXN_ID, txnId, json.dumps(reply),
                                   clientId, reqId, TXN_ID, txnId))

    def addMerkleDataForTxn(self, txnId, serialNo, STH, auditInfo):
        auditInfo = ", ".join(["'{}'".format(h) for h in auditInfo])
        self.client.command("""update {} set {} = '{}', serialNo = {},
        STH = '{}', auditInfo = [{}] upsert where {} = '{}'""".
                            format(TXN_DATA, TXN_ID, txnId, serialNo,
                                   json.dumps(STH), auditInfo, TXN_ID, txnId))

    def getReply(self, identifier, reqId):
        result = self.client.command("select reply from {} where clietId = '{}'"
                                     " and reqId = {}".
                                     format(TXN_DATA, identifier, reqId))
        return None if not result else json.loads(result[0].oRecordData['reply'])

    def getRepliesForTxnIds(self, *txnIds, serialNo=None):
        txnIds = ",".join(["'{}'".format(tid) for tid in txnIds])
        cmd = "select serialNo, reply from {} where {} in [{}]".\
            format(TXN_DATA, TXN_ID, txnIds)
        if serialNo:
            cmd += " and serialNo > {}".format(serialNo)
        result = self.client.command(cmd)
        return {r.oRecordData["serialNo"]: json.loads(r.oRecordData["reply"])[2]
                for r in result}
