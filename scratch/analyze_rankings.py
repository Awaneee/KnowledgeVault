import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.intent_category import IntentCategory
from app.models.note_intent_assignment import NoteIntentAssignment
from app.models.notes import Note
from app.services.chunk_service import ChunkService
from app.services.intent_category_service import IntentCategoryService

DATABASE_URL = "postgresql://postgres:postgres@127.0.0.1:5433/knowledgevault"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

csv_path = "evaluation_results/evaluation_results.csv"

semantic = {}
hybrid = {}

with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        bid = row["benchmark_id"]
        strat = row["strategy"]
        if strat == "semantic":
            semantic[bid] = row
        elif strat == "hybrid":
            hybrid[bid] = row

print("COMPARING ORDERED RETRIEVAL LISTS (SEMANTIC VS HYBRID):")
print("-----------------------------------------------------")

identical_count = 0
differing_order_count = 0
differing_items_count = 0

chunk_service = ChunkService(session)
intent_service = IntentCategoryService(session)

for bid in sorted(semantic.keys(), key=int):
    s_list = [int(x) for x in semantic[bid]["retrieved_note_ids"].split(",") if x]
    h_list = [int(x) for x in hybrid[bid]["retrieved_note_ids"].split(",") if x]
    query = semantic[bid]["query"]
    
    if s_list == h_list:
        identical_count += 1
        # Let's inspect this query to see if intent could have helped or did not
        # Let's check intent extraction and category matches for this query
        intent = intent_service.extractor.extract_query_intent_fast(query)
        cat_matches = intent_service.find_category_matches_for_query(query, user_id=1, limit=5)
        
        # Print info for queries where relevant notes were not fully retrieved (i.e. recall < 1)
        sem_recall = float(semantic[bid]["recall_at_k"])
        if sem_recall < 1.0:
            print(f"\nQuery {bid}: {query!r}")
            print(f"  Recall: {sem_recall:.3f} | Relevant: {semantic[bid]['relevant_note_ids']}")
            print(f"  Semantic / Hybrid Rank: {s_list}")
            print(f"  Extracted Intent: {intent['intent_type']} | Confidence: {intent['confidence']:.2f}")
            print(f"  Category Matches:")
            for m in cat_matches:
                print(f"    - Category: {m.category.name!r} | Score: {m.score:.3f} | Method: {m.method!r} | Distance: {m.distance}")
            
            # Let's find out if any missing relevant notes were in the matched categories!
            relevant_notes = [int(x) for x in semantic[bid]["relevant_note_ids"].split(",") if x]
            missing_notes = [nid for nid in relevant_notes if nid not in s_list]
            for mnid in missing_notes:
                # Find category assignment for missing note
                assignment = session.query(NoteIntentAssignment).filter(NoteIntentAssignment.note_id == mnid).first()
                if assignment:
                    cat = session.query(IntentCategory).filter(IntentCategory.id == assignment.intent_category_id).first()
                    print(f"    * Missing note [{mnid}] is in category: {cat.name!r}")
                    # Is this category in the matched categories?
                    matched_names = [m.category.name for m in cat_matches]
                    if cat.name in matched_names:
                        print(f"      => OPPORTUNITY: Category {cat.name!r} WAS MATCHED, but note [{mnid}] was not promoted!")
                    else:
                        print(f"      => NO OPPORTUNITY: Category {cat.name!r} was NOT matched by query categories.")
                else:
                    print(f"    * Missing note [{mnid}] has no category assignment.")
    else:
        # Check if same items but different order
        if set(s_list) == set(h_list):
            differing_order_count += 1
            print(f"\nQuery {bid} (DIFFERING ORDER): {query!r}")
            print(f"  SEMANTIC: {s_list}")
            print(f"  HYBRID:   {h_list}")
        else:
            differing_items_count += 1
            print(f"\nQuery {bid} (DIFFERING ITEMS): {query!r}")
            print(f"  SEMANTIC: {s_list}")
            print(f"  HYBRID:   {h_list}")

print("\n-----------------------------------------------------")
print(f"Identical: {identical_count} | Differing Order: {differing_order_count} | Differing Items: {differing_items_count}")

session.close()
