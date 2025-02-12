package com.example.myapplication

import android.os.Bundle
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView

class ItemsActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_items)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }
        val itemList:RecyclerView = findViewById(R.id.itemsList);
        val items = arrayListOf<Item>();
        items.add(Item(1,"apple","Apple","Good apple","some text for apple",130))
        items.add(Item(2,"gold_apple","Goldapple","Good gold apple","some text for gold apple",220))
        items.add(Item(3,"red apple","Redapple","Good red apple","some text for good red apple",220))
        items.add(Item(4,"red apple","Redapple","Good red apple","some text for good red apple",220))
        items.add(Item(5,"red apple","Redapple","Good red apple","some text for good red apple",220))
        items.add(Item(6,"red apple","Redapple","Good red apple","some text for good red apple",220))
        items.add(Item(7,"red apple","Redapple","Good red apple","some text for good red apple",220))
        items.add(Item(8,"red apple","Redapple","Good red apple","some text for good red apple",220))
        items.add(Item(9,"red apple","Redapple","Good red apple","some text for good red apple",220))
        items.add(Item(10,"bottle","Redapple","Good bottle","some text for bottle",310))
        itemList.layoutManager=LinearLayoutManager(this)
        itemList.adapter=ItemsAdapter(items,this)
    }
}