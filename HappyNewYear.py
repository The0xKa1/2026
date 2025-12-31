import os
import datetime
import subprocess

patterns = {
    '2': [
        [0, 1, 0, 0, 0, 1, 1], 
        [1, 0, 0, 0, 1, 0, 1],
        [1, 0, 0, 1, 0, 0, 1], 
        [1, 1, 1, 0, 0, 0, 1], 
    ],
    '0': [
        [0, 1, 1, 1, 1, 1, 0],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [0, 1, 1, 1, 1, 1, 0],
    ],
    '6': [
        [0, 0, 1, 1, 1, 1, 0], 
        [0, 1, 0, 1, 0, 0, 1],
        [1, 0, 0, 1, 0, 0, 1],
        [0, 0, 0, 0, 1, 1, 0], 
    ],
    'SPACE': [
        [0, 0, 0, 0, 0, 0, 0],
    ]
}

word_map = []
def add_char(char):
    word_map.extend(patterns[char])
    word_map.extend(patterns['SPACE'])

add_char('2')
add_char('0')
add_char('2')
add_char('6')


def run_git_commit(date_str):
    env = os.environ.copy()
    env['GIT_AUTHOR_DATE'] = f"{date_str} 12:00:00"
    env['GIT_COMMITTER_DATE'] = f"{date_str} 12:00:00"
    
    subprocess.run(
        ['git', 'commit', '--allow-empty', '-m', f"Pixel Art: {date_str}"],
        env=env,
        check=True
    )



def preview_graph(matrix):
    days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    print("\n--- GitHub Contribution Graph Preview ---")
    print("     " + " ".join(["" for _ in range(len(matrix))])) # Header padding
    for row_idx in range(7):
        line = f"{days[row_idx]} "
        
        for col in matrix:
            pixel = col[row_idx]
            line += "🟩" if pixel == 1 else "⬜"
            
        print(line)
    print("\n---------------------------------------------------")
def main():
    preview_graph(word_map)
    
    today = datetime.date.today()
    idx = (today.weekday() + 1) % 7 
    last_sunday = today - datetime.timedelta(days=idx)
    
    start_date = last_sunday - datetime.timedelta(weeks=30)
    
    current_date = start_date

    for col_idx, column in enumerate(word_map):
        for row_idx, pixel in enumerate(column):
            if pixel == 1:
                commit_date = current_date + datetime.timedelta(days=row_idx)
            
                for _ in range(5):
                    run_git_commit(commit_date)
                    
        current_date += datetime.timedelta(weeks=1)
        
if __name__ == "__main__":
    main()