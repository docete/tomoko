**flush implementation in `internalFlushcache`**

    boolean internalFlushcache(
      final HLog wal, final long myseqid, MonitoredTask status)
    {
      MultiVersionConsistencyControl.WriteEntry w = null;
      
      // block updates while snapshot the memstore of all stores
      this.updatesLock.writeLock().lock();
      try {
        w = mvcc.beginMemStoreInsert();
        mvcc.advanceMemstore(w);
    
        for (Store s : stores.values()) {
          storeFlushers.add(s.getStoreFlusher(completeSequenceId));
        }
    
        // prepare flush (take a snapshot
        for (StoreFlusher flusher : storeFlushers) {
          flusher.prepare();
        }
      } finally {
        this.updatesLock.writeLock().unlock();
      }
    }
