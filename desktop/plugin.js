import { PANES_AREA, STATUSBAR_AREAS, TRANSCRIPT_DIRECTIVE_AREA, host } from '@hermes/plugin-sdk';
import { useState } from 'react';
import { jsx, jsxs } from 'react/jsx-runtime';

function OmniSightDirectiveCard({ attrs }) {
  const [sliderPos, setSliderPos] = useState(50);
  const [status, setStatus] = useState((attrs && attrs.status) || 'healed');

  const diffId = (attrs && attrs.id) || 'diff_49b';
  const beforeDefects = (attrs && attrs.before_defects) || '2';
  const afterDefects = (attrs && attrs.after_defects) || '0';

  const handleApprove = () => {
    setStatus('applied');
    const cmd = `omnisight_verify_layout(expected_clean=true)`;
    if (host && host.composer && typeof host.composer.submit === 'function') {
      host.composer.submit(null, cmd);
    } else if (host && host.composer && typeof host.composer.insertText === 'function') {
      host.composer.insertText(null, cmd);
    }
  };

  return jsxs('div', {
    style: {
      border: '1px solid var(--ui-stroke-secondary, var(--ui-border))',
      borderRadius: '10px',
      background: 'var(--card, var(--ui-surface-2))',
      color: 'var(--foreground, var(--ui-text-primary))',
      padding: '12px 14px',
      margin: '6px 0',
      fontSize: '12px'
    },
    children: [
      jsxs('div', {
        style: { display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' },
        children: [
          jsxs('div', {
            style: { display: 'flex', alignItems: 'center', gap: '8px' },
            children: [
              jsx('span', { style: { fontFamily: 'var(--ui-font-mono)', color: 'var(--ui-accent)', fontWeight: 700 }, children: '👁️ OMNISIGHT' }),
              jsx('span', { style: { fontWeight: 600 }, children: `Visual Verification · ${diffId}` }),
              jsx('span', {
                style: {
                  fontSize: '10px',
                  padding: '2px 6px',
                  borderRadius: '4px',
                  background: status === 'applied' ? 'rgba(35, 134, 54, 0.2)' : 'rgba(0, 210, 255, 0.15)',
                  color: 'var(--ui-accent)'
                },
                children: status === 'applied' ? 'APPLIED' : 'HEALED'
              })
            ]
          }),
          jsx('span', {
            style: { fontFamily: 'var(--ui-font-mono)', fontSize: '11px', color: 'var(--ui-text-secondary)' },
            children: `Defects: ${beforeDefects} → ${afterDefects}`
          })
        ]
      }),
      jsxs('div', {
        style: {
          position: 'relative',
          width: '100%',
          height: '110px',
          borderRadius: '6px',
          overflow: 'hidden',
          border: '1px solid var(--ui-stroke-secondary, var(--ui-border))',
          background: 'var(--ui-surface-1, rgba(255,255,255,0.03))',
          marginTop: '6px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          padding: '8px'
        },
        children: [
          jsxs('div', {
            style: { display: 'flex', justifyContent: 'space-between', marginBottom: '6px', fontSize: '11px', fontFamily: 'var(--ui-font-mono)' },
            children: [
              jsx('span', { style: { color: 'var(--ui-text-secondary)' }, children: Number(beforeDefects) > 0 ? `◀ BEFORE: ${beforeDefects} Defect(s)` : '◀ BEFORE: Clean' }),
              jsx('span', { style: { color: 'var(--ui-accent)' }, children: Number(afterDefects) === 0 ? 'AFTER: Zero Collisions ▶' : `AFTER: ${afterDefects} Defect(s) Remaining ▶` })
            ]
          }),
          jsx('input', {
            type: 'range',
            min: '0',
            max: '100',
            value: sliderPos,
            onChange: (e) => setSliderPos(Number(e.target.value)),
            style: { width: '100%', cursor: 'ew-resize', accentColor: 'var(--ui-accent)' }
          }),
          jsxs('div', {
            style: { display: 'flex', justifyContent: 'space-between', marginTop: '6px', fontSize: '10px', color: 'var(--ui-text-secondary)' },
            children: [
              jsx('span', { children: `Split: ${sliderPos}% Before` }),
              jsx('span', { children: `Mobile Viewport (393px): 0 Blowouts` }),
              jsx('span', { children: `${100 - sliderPos}% Healed` })
            ]
          })
        ]
      }),
      jsxs('div', {
        style: { display: 'flex', justifyContent: 'flex-end', marginTop: '10px' },
        children: [
          jsx('button', {
            onClick: handleApprove,
            disabled: status === 'applied',
            style: {
              padding: '5px 14px',
              borderRadius: '6px',
              border: 'none',
              background: 'var(--ui-accent)',
              color: 'var(--card, var(--ui-surface-2))',
              fontWeight: 600,
              cursor: status === 'applied' ? 'default' : 'pointer',
              fontSize: '11px'
            },
            children: status === 'applied' ? '✓ Layout Applied' : '✓ Approve & Apply Fix'
          })
        ]
      })
    ]
  });
}

function OmniSightSidebarPane() {
  return jsxs('div', {
    style: { padding: '12px', color: 'var(--foreground, var(--ui-text-primary))', fontFamily: 'var(--ui-font-mono)', fontSize: '12px' },
    children: [
      jsx('div', { style: { fontWeight: 700, color: 'var(--ui-accent)', marginBottom: '8px' }, children: '👁️ OMNISIGHT SPATIAL CORTEX' }),
      jsx('div', { style: { color: 'var(--ui-text-secondary)', marginBottom: '12px' }, children: 'Active layout tracking & AST-to-pixel bidirectional mapping.' }),
      jsxs('div', {
        style: { border: '1px solid var(--ui-stroke-secondary, var(--ui-border))', borderRadius: '6px', padding: '8px' },
        children: [
          jsx('div', { style: { color: 'var(--ui-accent)', fontWeight: 600 }, children: 'Surface Inspection Pipeline' }),
          jsx('div', { style: { fontSize: '11px', marginTop: '4px' }, children: '• Chrome CDP WebSocket: :9222' }),
          jsx('div', { style: { fontSize: '11px' }, children: '• Responsive Geometry Engine: Ready' }),
          jsx('div', { style: { fontSize: '11px' }, children: '• AST Source Map: data-hermes-source' })
        ]
      })
    ]
  });
}

function OmniSightStatusPill() {
  return jsx('span', {
    style: { fontFamily: 'var(--ui-font-mono)', fontSize: '11px', color: 'var(--ui-accent)' },
    children: '👁️ omnisight:tracking'
  });
}

export default {
  id: 'omnisight',
  name: 'OmniSight',
  register(ctx) {
    ctx.register({
      id: 'omnisight-diff',
      area: TRANSCRIPT_DIRECTIVE_AREA,
      data: {
        name: 'omnisight-diff',
        render: ({ attrs }) => jsx(OmniSightDirectiveCard, { attrs }),
      }
    });

    ctx.register({
      id: 'omnisight',
      area: PANES_AREA,
      title: 'OmniSight',
      data: { placement: 'right', width: '300px' },
      render: () => jsx(OmniSightSidebarPane, {})
    });

    ctx.register({
      id: 'omnisight-status',
      area: STATUSBAR_AREAS.right,
      order: 100,
      render: () => jsx(OmniSightStatusPill, {})
    });
  }
};