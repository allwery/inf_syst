package com.example.myapplication

import android.content.Context
import android.content.Intent
import android.media.Image
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView

class ItemsAdapter(var items:List<Item>,var context:Context):RecyclerView.Adapter<ItemsAdapter.MyViewHolder>() {
    class MyViewHolder(view:View):RecyclerView.ViewHolder(view){

        val button:Button=view.findViewById(R.id.button_item)
        val textView1:TextView=view.findViewById(R.id.textView_item)
        val textView2:TextView=view.findViewById(R.id.textView2_item)
        val textView3:TextView=view.findViewById(R.id.textView3_item)
        val image:ImageView=view.findViewById(R.id.imageView_item)

    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): MyViewHolder {
       val view=LayoutInflater.from(parent.context).inflate(R.layout.item_in_list,parent,false)
        return MyViewHolder(view)
    }

    override fun getItemCount(): Int {
        return items.count()
    }

    override fun onBindViewHolder(holder: MyViewHolder, position: Int) {
        holder.textView1.text=items[position].title
        holder.textView2.text=items[position].description
        holder.textView3.text= items[position].price.toString()
        val imageId=context.resources.getIdentifier(items[position].image,"drawable",context.packageName)
        holder.image.setImageResource(imageId)
        holder.button.setOnClickListener {
            val intent= Intent(context,ItemActivity::class.java)
            intent.putExtra("itemTitle",items[position].title)
            intent.putExtra("itemDescription",items[position].description)
            intent.putExtra("itemPrice",items[position].price)
            context.startActivity(intent)
        }
    }
}