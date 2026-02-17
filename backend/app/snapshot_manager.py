import asyncio
from .crdt_manager import crdt_manager
from .document_service import DocumentService


class SnapshotManager:

    def __init__(self):

        self.pending_snapshots = set()

        self.interval = 5  # seconds

        self.task = None


    async def start(self):

        if self.task is None:

            self.task = asyncio.create_task(self.snapshot_loop())


    def mark_dirty(self, document_id):

        self.pending_snapshots.add(document_id)


    async def snapshot_loop(self):

        print("Snapshot manager started")

        while True:

            await asyncio.sleep(self.interval)

            await self.flush_snapshots()


    async def flush_snapshots(self):

        if not self.pending_snapshots:
            return

        print(f"Saving snapshots: {self.pending_snapshots}")

        for document_id in list(self.pending_snapshots):

            try:

                doc = crdt_manager.get_document(document_id)

                content = doc.get_text()

                await DocumentService.save_document(
                    document_id,
                    content
                )

            except Exception as e:

                print("Snapshot error:", e)

        self.pending_snapshots.clear()


snapshot_manager = SnapshotManager()
