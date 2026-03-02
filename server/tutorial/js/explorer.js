// ============================================================
// Chain Explorer — CMPUT 802  |  Vanilla JS
// ============================================================

(function () {
  'use strict';

  // ------- State -------
  let chain = [];
  let status = null;
  let currentBlockIndex = 0;
  let autoRefreshInterval = null;
  const REFRESH_MS = 10000;

  // ------- DOM refs -------
  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => document.querySelectorAll(sel);

  const els = {
    chainLength: $('#statChainLength'),
    difficulty: $('#statDifficulty'),
    targetPrefix: $('#statTargetPrefix'),
    latestHash: $('#statLatestHash'),
    chainInner: $('#chainInner'),
    chainBadge: $('#chainBadge'),
    blockViewer: $('#blockViewer'),
    blockIndexInput: $('#blockIndexInput'),
    blockTotal: $('#blockTotal'),
    btnPrev: $('#btnPrev'),
    btnNext: $('#btnNext'),
    ledgerBody: $('#ledgerBody'),
    ledgerBadge: $('#ledgerBadge'),
    lastUpdated: $('#lastUpdated'),
    autoRefreshToggle: $('#autoRefreshToggle'),
  };

  // ------- API Fetchers -------

  async function fetchJSON(url) {
    const res = await fetch(url);
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}: ${res.statusText}`);
    }
    return res.json();
  }

  async function fetchStatus() {
    return fetchJSON('/status');
  }

  async function fetchChain() {
    return fetchJSON('/chain');
  }

  async function fetchLatest() {
    return fetchJSON('/latest');
  }

  async function fetchBlock(index) {
    return fetchJSON(`/block/${index}`);
  }

  // ------- Utility -------

  function truncateHash(hash, len) {
    if (!hash) return '--';
    len = len || 12;
    if (hash.length <= len * 2) return hash;
    return hash.slice(0, len) + '...' + hash.slice(-len);
  }

  function formatTimestamp(ts) {
    if (ts === 0 || ts === 0.0) return 'Genesis (epoch 0)';
    try {
      const d = new Date(ts * 1000);
      return d.toLocaleString('en-CA', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false,
      });
    } catch {
      return String(ts);
    }
  }

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
  }

  function copyToClipboard(text, btn) {
    navigator.clipboard.writeText(text).then(function () {
      btn.classList.add('copied');
      btn.innerHTML = '&#10003;';
      setTimeout(function () {
        btn.classList.remove('copied');
        btn.innerHTML = '&#9112;';
      }, 1500);
    }).catch(function () {
      // fallback
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.left = '-9999px';
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      btn.classList.add('copied');
      btn.innerHTML = '&#10003;';
      setTimeout(function () {
        btn.classList.remove('copied');
        btn.innerHTML = '&#9112;';
      }, 1500);
    });
  }

  function nowTimestamp() {
    const d = new Date();
    return d.toLocaleTimeString('en-CA', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false });
  }

  // ------- Render: Status Cards -------

  function renderStatus(data) {
    status = data;
    els.chainLength.textContent = data.chain_length;
    els.difficulty.textContent = data.difficulty;
    els.targetPrefix.textContent = '"' + data.target_prefix + '"';
    els.latestHash.textContent = truncateHash(data.latest_hash, 16);
    els.latestHash.setAttribute('data-tooltip', data.latest_hash);
    els.latestHash.onclick = function () {
      copyToClipboard(data.latest_hash, els.latestHash);
    };
  }

  // ------- Render: Chain Visualization -------

  function renderChain(blocks) {
    chain = blocks;
    els.chainBadge.textContent = blocks.length + ' block' + (blocks.length !== 1 ? 's' : '');

    if (!blocks.length) {
      els.chainInner.innerHTML = '<div class="ex-chain-empty">No blocks in chain.</div>';
      return;
    }

    let html = '';
    for (let i = 0; i < blocks.length; i++) {
      const b = blocks[i];
      const isGenesis = i === 0;
      const isActive = i === currentBlockIndex;
      const email = b.data && b.data.miner_email ? b.data.miner_email : '--';
      const hashShort = b.hash ? b.hash.slice(0, 8) : '--------';

      if (i > 0) {
        html += '<div class="ex-chain-link"><div class="ex-chain-link-dot"></div></div>';
      }

      html += '<div class="ex-block-card' +
        (isGenesis ? ' genesis' : '') +
        (isActive ? ' active' : '') +
        '" data-index="' + i + '">' +
        '<div class="ex-block-num">Block #' + b.index + '</div>' +
        '<div class="ex-block-miner">' + escapeHtml(email) + '</div>' +
        '<div class="ex-block-hash">' + hashShort + '</div>' +
        '</div>';
    }

    els.chainInner.innerHTML = html;

    // Click handlers on block cards
    var cards = els.chainInner.querySelectorAll('.ex-block-card');
    cards.forEach(function (card) {
      card.addEventListener('click', function () {
        var idx = parseInt(this.getAttribute('data-index'), 10);
        navigateToBlock(idx);
      });
    });

    // Scroll to show active block
    scrollToActiveBlock();
  }

  function scrollToActiveBlock() {
    var active = els.chainInner.querySelector('.ex-block-card.active');
    if (active) {
      active.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
    }
  }

  function updateChainActive() {
    var cards = els.chainInner.querySelectorAll('.ex-block-card');
    cards.forEach(function (card) {
      var idx = parseInt(card.getAttribute('data-index'), 10);
      if (idx === currentBlockIndex) {
        card.classList.add('active');
      } else {
        card.classList.remove('active');
      }
    });
  }

  // ------- Render: Block Viewer -------

  function renderBlockViewer(block) {
    if (!block) {
      els.blockViewer.innerHTML = '<div class="ex-loading">No block data.</div>';
      return;
    }

    var data = block.data || {};

    function hashRow(label, value, extraClass) {
      var cls = extraClass ? ' ' + extraClass : '';
      var truncated = truncateHash(value, 20);
      var isTruncated = value && value.length > 40;
      return '<div class="ex-detail-row">' +
        '<div class="ex-detail-key">' + escapeHtml(label) + '</div>' +
        '<div class="ex-detail-val' + cls + '">' +
        (isTruncated
          ? '<span class="ex-truncate ex-tooltip" data-tooltip="' + escapeHtml(value) + '">' + escapeHtml(truncated) + '</span>'
          : '<span>' + escapeHtml(value || '--') + '</span>') +
        (value && value.length > 8
          ? ' <button class="ex-copy-btn" data-copy="' + escapeHtml(value) + '" title="Copy">&#9112;</button>'
          : '') +
        '</div></div>';
    }

    function textRow(label, value, extraClass) {
      var cls = extraClass ? ' ' + extraClass : '';
      var display = (value === null || value === undefined) ? '--' : String(value);
      return '<div class="ex-detail-row">' +
        '<div class="ex-detail-key">' + escapeHtml(label) + '</div>' +
        '<div class="ex-detail-val' + cls + '">' + escapeHtml(display) + '</div>' +
        '</div>';
    }

    var html = '<div class="ex-block-detail">';
    // Block header fields
    html += textRow('Index', block.index, 'accent');
    html += textRow('Timestamp', formatTimestamp(block.timestamp));
    html += hashRow('Previous Hash', block.previous_hash);
    html += textRow('Nonce', block.nonce.toLocaleString());
    html += hashRow('Hash', block.hash, 'accent');
    html += hashRow('Signature', block.signature);

    // Data section header
    html += '<div class="ex-detail-section-header">Block Data</div>';
    html += hashRow('Miner Pubkey', data.miner_pubkey);
    html += textRow('Miner Email', data.miner_email);
    html += textRow('Action', data.action);
    html += textRow('Student Random', data.student_random ? JSON.stringify(data.student_random) : '--');
    html += textRow('Instructor Random', data.instructor_random ? JSON.stringify(data.instructor_random) : '--');

    html += '</div>';

    els.blockViewer.innerHTML = html;

    // Wire up copy buttons
    els.blockViewer.querySelectorAll('.ex-copy-btn').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        copyToClipboard(this.getAttribute('data-copy'), this);
      });
    });
  }

  function updateNavState() {
    var maxIndex = chain.length - 1;
    els.btnPrev.disabled = currentBlockIndex <= 0;
    els.btnNext.disabled = currentBlockIndex >= maxIndex;
    els.blockIndexInput.value = currentBlockIndex;
    els.blockIndexInput.max = maxIndex;
    els.blockTotal.textContent = '/ ' + maxIndex;
  }

  function navigateToBlock(index) {
    if (index < 0) index = 0;
    if (index >= chain.length) index = chain.length - 1;
    currentBlockIndex = index;
    updateNavState();
    updateChainActive();
    scrollToActiveBlock();

    // Use cached chain data if available
    if (chain[index]) {
      renderBlockViewer(chain[index]);
    } else {
      // Fetch from server as fallback
      els.blockViewer.innerHTML = '<div class="ex-loading"><div class="ex-spinner"></div> Loading block...</div>';
      fetchBlock(index)
        .then(function (block) { renderBlockViewer(block); })
        .catch(function (err) { showBlockError(err.message); });
    }
  }

  function showBlockError(msg) {
    els.blockViewer.innerHTML =
      '<div class="ex-error"><span class="ex-error-icon">&#x26A0;</span> ' +
      escapeHtml(msg) + '</div>';
  }

  // ------- Render: Ledger Table -------

  function renderLedger(ledger) {
    if (!ledger || Object.keys(ledger).length === 0) {
      els.ledgerBody.innerHTML =
        '<tr><td class="ex-table-empty" colspan="3">No students in the ledger yet. Mine a block to appear here.</td></tr>';
      els.ledgerBadge.textContent = '0 students';
      return;
    }

    var entries = Object.entries(ledger);
    entries.sort(function (a, b) {
      // Sort completed first (status 1 before 0), then alphabetically
      if (a[1].status !== b[1].status) return b[1].status - a[1].status;
      return a[0].localeCompare(b[0]);
    });

    var completed = entries.filter(function (e) { return e[1].status === 1; }).length;
    els.ledgerBadge.textContent = completed + '/' + entries.length + ' complete';

    var html = '';
    entries.forEach(function (entry) {
      var email = entry[0];
      var info = entry[1];
      var isComplete = info.status === 1;

      html += '<tr>';
      html += '<td>' + escapeHtml(email) + '</td>';
      html += '<td>';
      if (isComplete) {
        html += '<span class="ex-badge ex-badge-complete"><span class="ex-badge-dot"></span>Complete</span>';
      } else {
        html += '<span class="ex-badge ex-badge-pending"><span class="ex-badge-dot"></span>Pending</span>';
      }
      html += '</td>';
      html += '<td>' + (info.block_index !== undefined && info.block_index !== null ? info.block_index : '--') + '</td>';
      html += '</tr>';
    });

    els.ledgerBody.innerHTML = html;
  }

  // ------- Data Loading -------

  function showGlobalError(msg) {
    var errDiv = document.createElement('div');
    errDiv.className = 'ex-error';
    errDiv.style.margin = '0 0 20px';
    errDiv.innerHTML = '<span class="ex-error-icon">&#x26A0;</span> ' + escapeHtml(msg);
    var main = $('main.ex-main');
    main.insertBefore(errDiv, main.firstChild);
    setTimeout(function () { errDiv.remove(); }, 8000);
  }

  async function loadAllData() {
    try {
      var results = await Promise.all([fetchStatus(), fetchChain()]);
      var statusData = results[0];
      var chainData = results[1];

      renderStatus(statusData);
      renderChain(chainData);
      renderLedger(statusData.ledger);

      // Update block viewer
      if (currentBlockIndex >= chainData.length) {
        currentBlockIndex = chainData.length - 1;
      }
      updateNavState();
      navigateToBlock(currentBlockIndex);

      // Update timestamp
      els.lastUpdated.textContent = 'Updated ' + nowTimestamp();
    } catch (err) {
      showGlobalError('Failed to load data: ' + err.message);
    }
  }

  // ------- Auto Refresh -------

  function startAutoRefresh() {
    stopAutoRefresh();
    autoRefreshInterval = setInterval(function () {
      loadAllData();
    }, REFRESH_MS);
  }

  function stopAutoRefresh() {
    if (autoRefreshInterval) {
      clearInterval(autoRefreshInterval);
      autoRefreshInterval = null;
    }
  }

  // ------- Event Listeners -------

  function initEvents() {
    // Prev / Next buttons
    els.btnPrev.addEventListener('click', function () {
      navigateToBlock(currentBlockIndex - 1);
    });

    els.btnNext.addEventListener('click', function () {
      navigateToBlock(currentBlockIndex + 1);
    });

    // Direct index input
    els.blockIndexInput.addEventListener('change', function () {
      var val = parseInt(this.value, 10);
      if (!isNaN(val)) {
        navigateToBlock(val);
      }
    });

    els.blockIndexInput.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') {
        var val = parseInt(this.value, 10);
        if (!isNaN(val)) {
          navigateToBlock(val);
        }
      }
    });

    // Auto-refresh toggle
    els.autoRefreshToggle.addEventListener('change', function () {
      if (this.checked) {
        startAutoRefresh();
      } else {
        stopAutoRefresh();
      }
    });

    // Keyboard navigation
    document.addEventListener('keydown', function (e) {
      // Only if not focused on an input
      if (document.activeElement && document.activeElement.tagName === 'INPUT') return;
      if (e.key === 'ArrowLeft') {
        navigateToBlock(currentBlockIndex - 1);
      } else if (e.key === 'ArrowRight') {
        navigateToBlock(currentBlockIndex + 1);
      }
    });
  }

  // ------- Init -------

  function init() {
    initEvents();
    loadAllData();
  }

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
