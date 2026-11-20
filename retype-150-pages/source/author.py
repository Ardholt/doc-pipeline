"""Compose the original field notebook. OCR never imports this module."""
import json
from pathlib import Path

TOPICS = [
('RECEIPT CHECK', 'A package is counted before it joins the working stock. The outer label is useful for routing, but the contents decide the record. Open one container at a time and keep its loose pieces together until the count is complete.', 'If the label and the contents disagree, preserve both readings in the note. A neat total is less useful than a traceable difference. Set the container aside without changing the label, then ask for a second count using the same unit.'),
('SHELF ORDER', 'A shelf is easiest to use when its order is visible from the aisle. Place the heavier containers on the lower level and keep each item code facing forward. Leave enough room to remove a container without disturbing the next one.', 'An empty space is part of the arrangement. Do not fill a gap merely because a small box will fit there. First check whether the gap marks an item awaiting return, a cleaning interval, or a limit on the load of that shelf.'),
('TOOL RETURN', 'A tool returns to service only after its condition has been checked. Brush away loose material and place the tool on the inspection mat. Compare the working edge with the condition recorded before use, and record any new mark in ordinary words.', 'A clean surface does not prove that a tool is ready. Check the joint, handle and retaining pin as separate parts. If a part is missing, mark the whole tool as held; never leave it in the ready tray beside complete tools.'),
('COUNTING METHOD', 'A count begins with a defined unit. Loose pieces, paired pieces and sealed packs must not share a column unless the conversion is written down. Read the unit aloud at the start of the count and repeat it when another person takes over.', 'Make a short tally after each group rather than carrying a long number in memory. When two counts differ, repeat the smaller group that contains the difference. Do not average the totals: the required result is a count, not an estimate.'),
('SURFACE CARE', 'A work surface should be cleared before it is cleaned. Move the loose items into a tray and retain their order. Use a dry cloth first so that coarse particles are removed rather than dragged across the surface during the next pass.', 'Inspect the edge as well as the centre. A narrow strip beneath a raised lip can hold material that is missed by a quick wipe. Record persistent marks separately from removable dirt so that tomorrow\'s check starts from the right condition.'),
('LABEL READING', 'Read a label from left to right before copying its code. Similar characters are a reason to slow down, especially where a faint stroke might be part of a letter. Compare the code with the item record only after making an initial reading.', 'Keep the old label when a replacement is fitted. Write down the reason for replacement and check that the new label identifies the same item. Clear lettering is helpful, but an attractive label attached to the wrong container creates a larger problem.'),
('DRY STORAGE', 'Dry storage depends on routine observation as well as closed lids. Check the seal before moving a container and look for a change in the paper liner. A small curl at an edge may be the first visible sign that conditions have changed.', 'Separate observations from explanations. Record a damp patch as a damp patch; do not record a leak unless its path has been found. Move the affected material to the holding shelf and preserve the arrangement that will help the next inspection.'),
('TRANSFER NOTE', 'A transfer note follows the material through each change of location. Record the starting shelf, destination code and quantity before the move. Keep the note with the tray until the receiving position has been checked against the written destination.', 'Complete a transfer only after the final count. If the move is interrupted, leave a clear status note and keep the unfinished tray separate. The next shift must be able to tell whether a quantity is waiting to move or has already arrived.'),
('MEASURING EDGE', 'A length reading begins at the marked zero rather than at the end of the rule. Hold the rule flat and keep the item square to the scale. Read from directly above the mark so that the edge does not hide the nearest division.', 'Record the unit beside the value every time. A bare number can travel into a later table and lose its meaning. If the mark lies between divisions, describe that position; extra decimal places do not make the reading more certain.'),
('HOLDING AREA', 'The holding area separates unresolved items from ready stock. Each tray needs one clear reason for being held and a next action that can be completed. A short specific note is better than a broad word that leaves the next reader guessing.', 'Review the oldest tray first, but do not release it merely because it has waited. Check that the stated reason has been resolved and preserve the evidence of that check. Move the material and its note together when the status changes.'),
('PACKING ORDER', 'Packing starts with the item that needs the most support. Arrange the remaining pieces so that none can move across a working edge. Check the container by lifting it gently before closing it; a shifting weight is a reason to open it again.', 'Leave the contents list on top of the inner wrapping. The next reader should not have to empty the container to discover what belongs inside. Keep a separate count for loose fittings and use the same names on the list and the record.'),
('SHIFT RECORD', 'A shift record explains what changed during the work period. Begin with unfinished actions carried forward, then add completed work in the order it occurred. Use short sentences that distinguish an observation, an action and a result.', 'Before closing the record, read it as if none of the events were familiar. Replace unclear pronouns with item codes and state where any held material can be found. A later reader needs the decision and its reason, not a reconstruction of the conversation.'),
('REPEAT CHECK', 'A repeat check should use the same method as the first check unless a change is recorded. Start with the same unit, position and grouping. This makes it possible to tell whether a different result comes from the material or from the method.', 'Do not erase the first result after a second result is obtained. Keep both values and describe the reason for repeating the work. Agreement supports the record; disagreement points to a question that still needs attention.'),
('SMALL REPAIR', 'A small repair begins with a decision about the boundary of the work. Identify the loose or damaged part and keep adjacent parts in their original order. Use a tray for removed fittings so that every piece can be accounted for at the end.', 'After the repair, check the function that was affected and the parts disturbed during access. Record what was changed rather than writing only that the item is fixed. A future inspection should be able to identify the repaired area without taking the item apart.'),
('CLOSING ROUND', 'The closing round leaves the area understandable for the next opening. Return ready items to their marked positions and gather unresolved work into the holding area. Check that every tray has a status note before switching off the task lighting.', 'Finish by reading the outstanding list against the physical trays. A written action without a tray may be complete; a tray without an action may be forgotten. Resolve the difference while the work is still fresh, and leave a brief reason for any remaining hold.'),
]
CONDITIONS = [
('a pale diagonal mark', 'The mark remained visible after a dry wipe. Its position was recorded so that a later check can tell whether it has spread.'),
('a loose inner divider', 'The divider was lifted out and placed beside the tray. The contents stayed in their original groups while the support was checked.'),
('a folded corner on the liner', 'The corner was opened without pulling the rest of the liner free. No loose pieces were found beneath the fold.'),
('a faint code on the upper face', 'The code was read twice under steady light. Both readings were retained because the final character needs another inspection.'),
('a narrow gap beside the insert', 'The gap was checked at each end. The note records the location rather than assuming that the insert has changed size.'),
('an uneven stack of thin pieces', 'The stack was divided into smaller groups on the mat. Each group was counted before the pieces were returned to the container.'),
('a light scuff near the rim', 'The scuff was compared with the earlier condition note. It was kept in the record even though it did not prevent the next check.'),
('a detached paper tab', 'The tab was kept with the tray rather than discarded. Its wording was copied into the record before a fresh tab was attached.'),
('a displaced protective strip', 'The strip was returned to its marked position after the edge was checked. The note records both the observation and the action.'),
('a small difference in the tally', 'The affected group was counted again from the beginning. The first tally remains in the record beside the second result.'),
]

def build():
    pages=[]
    for batch,(condition,action) in enumerate(CONDITIONS,1):
        for topic,(title,opening,caution) in enumerate(TOPICS,1):
            p=(batch-1)*len(TOPICS)+topic
            code=f'D{batch:02d}-{topic:02d}'
            ready=18+(p*7)%53; held=1+p%5; total=ready+held
            rows=[['Item','Ready','Held','Total'],[f'K{p:03d}',str(ready),str(held),str(total)],
                  [f'R{p:03d}',str(ready+4),str(held+1),str(total+5)]]
            blocks=[{'kind':'heading','text':f'{title} / {p:03d}'},
                    {'kind':'paragraph','text':f'Record {code}. Round {batch:02d}. Sheet {p:03d}.'},
                    {'kind':'paragraph','text':opening},
                    {'kind':'paragraph','text':f'The tray for item K{p:03d} showed {condition}. {action}'},
                    {'kind':'paragraph','text':caution},
                    {'kind':'heading','text':'COUNT RECORD'},
                    {'kind':'table','rows':rows},
                    {'kind':'paragraph','text':f'The first row records {ready} ready pieces and {held} held pieces, giving {total} in all. The second row is a separate group, not an addition to the first. Keep the two item codes distinct when copying these values into a later record.'},
                    {'kind':'paragraph','text':f'Closing note: retain record {code} with the tray until the next round. Check the status before moving the contents. A corrected entry must preserve the earlier reading and state why it changed; a blank space must never be treated as a zero.'}]
            pages.append({'id':f'page-{p:03d}','page':p,'blocks':blocks})
    return {'schema_version':1,'title':'Workshop Records','authorship':'Original procedural text by Genco Doganay; MIT. Composed before rendering or extraction. Repeated instructions and varied records are deliberate.','pages':pages}

if __name__=='__main__':
    path=Path(__file__).with_name('reference.json')
    if path.exists(): raise SystemExit('ERROR: reference already exists; refusing to overwrite')
    path.write_text(json.dumps(build(),indent=2,ensure_ascii=False)+'\n')
